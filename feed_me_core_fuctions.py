import random
import requests
import json
from bs4 import BeautifulSoup

from feed_me_support import (
    save_obj,
    screen_reset,
    recipe_source,
    display_recipe
)

from feed_me_refs import (
    dish_refs,
    cuisine_refs,
    method_refs,
    blank_recipe
)


def get_matching_recipes(recipes, name='none', cuisine='none', method='none', dish='none', season='none', ingredients=['none']):
    """Return list of recipes matching provided criteria from provided list of recipes"""

    return_recipes = []

    for recipe in recipes:
        criteria = [
            name in recipe['name'].lower() or name == 'none',
            cuisine == recipe['cuisine'] or cuisine == 'none',
            method == recipe['method'] or method == 'none',
            dish == recipe['dish'] or dish == 'none',
            season in recipe['season'] or season == 'none',
            any(item.title() in recipe['ingredients'] for item in ingredients) or ingredients == ['none'],
        ]

        if all(criteria):
            return_recipes.append(recipe)

    return return_recipes


def new_recipe_builder(url, source):
    """
    Build new recipe dictionary from compatiable URL.

            Parameters:
                    url (str): URL of recipe to be converted
                    source (str): Source of the URL from known sources

            Returns:
                    new_recipe (dict): Dictionary formatted to be added to recipe list

    """

    # Get page response via requests
    res = requests.get(url)
    # Parse response via beautiful soup
    soup = BeautifulSoup(res.text, 'html.parser')

    # Set exact recipe data from data element based on source
    if source == 'food_network':
        recipe_data = json.loads(soup.find('script', type='application/ld+json').text)[0]
    elif source == 'salt_and_lavender':
        recipe_data = json.loads(soup.find('script', type='application/ld+json').text)['@graph'][7]
    elif source == 'macheesemo':
        recipe_data = json.loads(soup.find_all('script', type='application/ld+json')[1].text)
    elif source in ['delish', 'bon_appetit']:
        recipe_data = json.loads(soup.find('script', type='application/ld+json').text)

    # Set recipe items

    # Set empty recipe dict
    new_recipe = {}
    # Set recipe name
    new_recipe['name'] = recipe_data['name']
    # Set recipe URL
    new_recipe['url'] = url
    # Set recipe ingredients
    new_recipe['ingredients'] = recipe_data['recipeIngredient']
    # Set recipe instructions
    new_recipe['instructions'] = recipe_data['recipeInstructions']
    # Set recipe yeild
    new_recipe['yeild'] = recipe_data['recipeYield']

    # Set recipe chef based on source
    if source == 'food_network':
        # Food Network chef
        new_recipe['chef'] = recipe_data['author'][0]['name']
    elif source in ['delish', 'salt_and_lavender', 'bon_appetit', 'macheesemo']:
        # All other defined sources
        new_recipe['chef'] = recipe_data['author']['name']

    # Set dish type from category based on source
    if 'recipeCategory' in recipe_data.keys():
        if source in ['food_network', 'bon_appetit', 'macheesemo']:
            if recipe_data['recipeCategory'] in dish_refs.keys():
                new_recipe['dish'] = dish_refs[recipe_data['recipeCategory']]
        elif source in ['delish', 'salt_and_lavender']:
            if recipe_data['recipeCategory'][0] in dish_refs.keys():
                new_recipe['dish'] = dish_refs[recipe_data['recipeCategory'][0]]
    else:
        new_recipe['dish'] = ''

    # Set cusine based on recipe name
    for cuisine_var, cuisine_std in cuisine_refs.items():
        if cuisine_var in new_recipe['name'].lower():
            new_recipe['cuisine'] = cuisine_std
            break
    else:
        new_recipe['cuisine'] = ''

    # Set method based on recipe name
    for method_var, method_std in method_refs.items():
        if method_var in new_recipe['name'].lower():
            new_recipe['method'] = method_std
            break
    else:
        new_recipe['method'] = ''

    return(new_recipe)


def add_recipe(recipes):
    # Set empty recipe
    new_recipe = blank_recipe

    # Reset screen
    screen_reset()

    # Determine method (url or manual)
    method = input("Enter 'url' to add a recipie from a website\nEnter 'manual' to add a recipe yourself:\n").lower()
    # Task selection loop
    if method not in ['url', 'manual']:
        method = input('Invalid entry. Re-Enter selection: ')

    # Reset screen
    screen_reset()

    # URL Processing
    if method == 'url':
        # Enter url
        url = input('Enter url to add: ')

        # Identify source
        source = recipe_source(url)

        # If unkown source revert to manual with option to exit
        if source == 'unknown':
            # Reset screen
            screen_reset()

            print('Unkown source')

        else:
            # If known source, set all possible fields
            new_recipe = new_recipe_builder(url, source)

    # Manual/Incomplte URL

    # Reset screen
    screen_reset()

    # Prompt user to fill in blank fields
    for field, value in new_recipe.items():
        if value in ['', 0, []]:
            entry = input(f'{field.title()} is blank. Enter the {field} for the recipe.\n')
            if field == 'yeild':
                entry = int(entry)
            elif field == 'instructions':
                entry = [entry]
            elif field == 'ingredients':
                entry = [entry]
            new_recipe[field] = entry

    # Add recipie to master list
    recipes.append(new_recipe)

    # Pickle new recipie list
    save_obj(recipes, 'recipes')

    # Reset screen
    screen_reset()

    # Add another recipie check
    add_again = input('Would you like to add another recipe? (y/n): ')
    while add_again.lower() not in ['y', 'n']:
        add_again = input('Would you like to add another recipe? (y/n): ')

    if add_again.lower() == 'y':
        add_recipe(recipes)


def find_recipe(recipes):
    search_fields = [
        {'name': 'Name', 'term': 'none'},
        {'name': 'Cuisine', 'term': 'none'},
        {'name': 'Method', 'term': 'none'},
        {'name': 'Dish', 'term': 'none'},
        {'name': 'Season', 'term': 'none'},
        {'name': 'Ingredients', 'term': 'none'},
    ]

    end_message = 'Undefined error.'

    # Reset screen
    screen_reset()

    # Describe search options
    print('Enter search term for each option. Leave blank and press enter to skip.')

    # Select search fields
    for idx, field in enumerate(search_fields, start=1):
        print(f"{idx} - {field['name']}")

    # Enter search criteria
    for field in search_fields:
        field['term'] = input(f"Enter search term for {field['name']}:\n")
        if field['term'] == '':
            field['term'] = 'none'

    # Conduct search
    eligible_recipies = get_matching_recipes(
        recipes,
        search_fields[0]['term'],
        search_fields[1]['term'],
        search_fields[2]['term'],
        search_fields[3]['term'],
        search_fields[4]['term'],
        [search_fields[5]['term']],
    )

    # Any result check
    if len(eligible_recipies) == 0:
        end_message = 'No Recipes Found'
        match_review = False
    else:
        match_review = True

    # Display results
    while match_review is True:
        # Reset screen
        screen_reset()

        # Randomly select recipe option
        recipe_option = random.choice(eligible_recipies)

        # Remove option from eligible recipes
        eligible_recipies.remove(recipe_option)

        # Display option
        display_recipe(recipe_option)

        # Prompt for next result or exit
        selection = input("Enter 'n' for the next recipe\nEnter 'q' to exit:\n")
        while selection not in ['n', 'q']:
            selection = input("Enter 'n' for the next recipe\nEnter 'q' to exit:\n")

        if selection == 'q':
            match_review = False
            end_message = 'Search Ended'
            break

        if len(eligible_recipies) == 0:
            # Reset screen
            screen_reset()
            # No more recipes message
            end_message = 'No other eligible recipes.'
            match_review = False
            break

    # Reset screen
    screen_reset()

    # Print end message
    print(end_message)

    # Search again check
    search_again = input('Would you like to try again? (y/n): ')
    while search_again.lower() not in ['y', 'n']:
        search_again = input('Would you like to try again? (y/n): ')

    if search_again.lower() == 'y':
        find_recipe(recipes)
