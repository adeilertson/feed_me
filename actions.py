from json.decoder import JSONDecodeError
import random
import requests
import json
from bs4 import BeautifulSoup

import support
import screens
import references
import db_actions


def get_matching_recipes(recipes, name='none', ingredients=['none']):
    """Return list of recipes matching provided criteria from provided list of recipes"""

    return_recipes = []

    for recipe in recipes:
        criteria = [
            name in recipe['name'].lower() or name == 'none',
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

    # Set empty recipe dict
    new_recipe = {}

    # Get page response via requests
    res = requests.get(url)
    # Parse response via beautiful soup
    soup = BeautifulSoup(res.text, 'html.parser')

    # Set exact recipe data from data element based on source
    if source == 'food_network':
        try:
            recipe_data = json.loads(soup.find('script', type='application/ld+json').text)[0]
        except JSONDecodeError:
            recipe_data = json.loads(soup.find('script', type='application/ld+json').string)[0]
        except AttributeError:
            recipe_data = json.loads(soup.find('script', type='application/json').string)
    elif source == 'salt_and_lavender':
        recipe_data = json.loads(soup.find('script', type='application/ld+json').text)['@graph'][7]
    elif source == 'macheesemo':
        recipe_data = json.loads(soup.find_all('script', type='application/ld+json')[1].text)
    elif source in ['delish', 'bon_appetit']:
        recipe_data = json.loads(soup.find('script', type='application/ld+json').text)  

    # Confirm data is recipe
    if 'name' not in recipe_data.keys():
       new_recipe['error'] = 'no_recipe_data'
       return(new_recipe)
    else:
        new_recipe['error'] = ''

    # Set recipe items

    # Set recipe name
    new_recipe['name'] = recipe_data['name']
    # Set recipe URL
    new_recipe['url'] = url
    # Clean and set recipe ingredients
    new_recipe['ingredients'] = [support.strip_html(ingredient) for ingredient in recipe_data['recipeIngredient']]
    # Set recipe yield
    new_recipe['yield'] = recipe_data['recipeYield']
    # Clean, format and set recipe instructions
    new_recipe['instructions'] = support.set_instructions(recipe_data['recipeInstructions'])

    # Set recipe chef based on source
    if type(recipe_data['author']) is list:
        new_recipe['chef'] = recipe_data['author'][0]['name']
    elif type(recipe_data['author']) is dict:
        new_recipe['chef'] = recipe_data['author']['name']
    else:
        new_recipe['chef'] = ''

    return(new_recipe)


def add_recipe():
    # Reset screen
    screens.screen_reset()

    # Determine method (url or manual)
    method = input("Enter 'url' to add a recipie from a website\nEnter 'manual' to add a recipe yourself:\n").lower()
    # Valid selection check
    if method not in ['url', 'manual']:
        cont = input('Invalid entry. Press enter to return to menu')
        return None

    # Reset screen
    screens.screen_reset()

    # URL Processing
    if method == 'url':
        # Enter url
        url = input('Enter url to add: ')

        # Identify source
        source = support.get_recipe_source(url)

        # If unkown source revert to manual with option to exit
        if source == 'unknown':
            # Reset screen
            screens.screen_reset()
            print('Unkown source')
            cont = input('Unkown source. Enter information manually? (y/n) ').lower()
            if cont == 'n':
                return None
        else:
            # Collect page data and attempt to parse recipe parts
            new_recipe = new_recipe_builder(url, source)

        # Bad/Unknown recipie structure URL
        if new_recipe['error'] == 'no_recipe_data':
            cont = input('Unable to get recipe from page. Confirm page has recipe data or try manual entry.\nPress enter to return to menu')

    # Manual/Incomplte URL
    # Reset screen
    screens.screen_reset()

    # Prompt user to fill in blank fields
    for field, value in new_recipe.items():
        if field == 'error':
            continue
        if value in ['', 0, []]:
            # Set yield
            if field == 'yield':
                entry = input('Yield is blank. Enter the yield for the recipe (ex. 4).\n')

            # Set instructions
            elif field == 'instructions':
                entry = input('Instructions is blank. Enter the instructions for the recipe. Copy/paste is recommended\n')

            # Set ingredients
            elif field == 'ingredients':
                text = input('Ingredients is blank. Enter the ingredients for the recipe separated by commas.\n')
                entry = text.split(',')

            # Set remaining fields with generic message
            else:
                entry = input(f'{field.title()} is blank. Enter the {field} for the recipe.\n')

            # Update field with new data
            new_recipe[field] = entry

    # Add recipie to database
    db_actions.add_recipe(new_recipe)

    # Reset screen
    screens.screen_reset()

    # Display recipe
    screens.display_recipe(new_recipe)
    cont = input('\nPress enter to conitnue. ')

    # Add another recipie check
    add_again = input('Would you like to add another recipe? (y/n): ')

    if add_again.lower() == 'y':
        add_recipe()


def find_recipe(recipes):
    search_fields = [
        {'name': 'Name', 'term': 'none'},
        {'name': 'Ingredients', 'term': 'none'},
    ]

    end_message = 'Undefined error.'

    # Reset screen
    screens.screen_reset()

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
        [search_fields[1]['term']],
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
        screens.screen_reset()

        # Randomly select recipe option
        recipe_option = random.choice(eligible_recipies)

        # Remove option from eligible recipes
        eligible_recipies.remove(recipe_option)

        # Display option
        screens.display_recipe(recipe_option)

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
            screens.screen_reset()
            # No more recipes message
            end_message = 'No other eligible recipes.'
            match_review = False
            break

    # Reset screen
    screens.screen_reset()

    # Print end message
    print(end_message)

    # Search again check
    search_again = input('Would you like to try again? (y/n): ')
    while search_again.lower() not in ['y', 'n']:
        search_again = input('Would you like to try again? (y/n): ')

    if search_again.lower() == 'y':
        find_recipe(recipes)


def delete_recipie():
    pass


def reset_recipie_table():
    screens.screen_reset()
    print('\nWARNING!\n\nResetting the recipie database will delete all stored recipies.')
    confirm = input('\nContinue? (y/n): ').lower()

    if confirm == 'y':
        db_actions.db_reset()
        cont = input('Press enter to return to admin menu')
