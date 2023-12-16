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
    # Set recipe ingredients
    new_recipe['ingredients'] = recipe_data['recipeIngredient']
    # Set recipe yeild
    new_recipe['yeild'] = recipe_data['recipeYield']

    # Set recipe instructions
    new_recipe['instructions'] = support.set_instructions(recipe_data['recipeInstructions'])

    # Set recipe chef based on source
    if type(recipe_data['author']) is list:
        new_recipe['chef'] = recipe_data['author'][0]['name']
    elif type(recipe_data['author']) is dict:
        new_recipe['chef'] = recipe_data['author']['name']
    else:
        new_recipe['chef'] = ''

    return(new_recipe)


def add_recipe(recipes, rec_retry=False):
    # Set empty recipe
    new_recipe = references.get_blank_recipe()

    # Reset screen
    support.screen_reset()

    # Determine method (url or manual)
    method = input("Enter 'url' to add a recipie from a website\nEnter 'manual' to add a recipe yourself:\n").lower()
    # Task selection loop
    if method not in ['url', 'manual']:
        method = input('Invalid entry. Re-Enter selection: ')

    # Reset screen
    support.screen_reset()

    # URL Processing
    if method == 'url':
        # Enter url
        url = input('Enter url to add: ')

        # Identify source
        source = support.get_recipe_source(url)

        # If unkown source revert to manual with option to exit
        if source == 'unknown':
            # Reset screen
            support.screen_reset()

            print('Unkown source')

        else:
            # If known source, set all possible fields
            new_recipe = new_recipe_builder(url, source)

    # Bad/Unknown recipie structure URL
    if new_recipe['error'] == 'no_recipe_data':
        print('Unable to get recipe from page. Confirm page has recipe data or try manual entry.')
        retry_url = input('Re-Enter URL? (y/n) ')
        # Retry URL loop
        if retry_url not in ['y', 'n']:
            method = input('Invalid entry. Re-Enter selection: ')
        
        # Retry options
        if retry_url == 'y':
            add_recipe(recipes, rec_retry=True)
        elif retry_url == 'n':
            return None

    # Manual/Incomplte URL

    # Reset screen
    support.screen_reset()

    # Prompt user to fill in blank fields
    for field, value in new_recipe.items():
        if field == 'error':
            continue
        if value in ['', 0, []]:
            # Set yield
            if field == 'yeild':
                entry = input('Yield is blank. Enter the yield for the recipe (ex. 4).\n')
                val_check = True
                while val_check is True:
                    try:
                        entry = int(entry)
                        val_check = False
                    except ValueError:
                        entry = input('Error. Re-Enter Yield as digits (ex. 4)')

            # Set instructions
            elif field == 'instructions':
                text = input('Instructions is blank. Enter the instructions for the recipe separated by at symbols (@).\n')
                entry = text.split('@')

            # Set ingredients
            elif field == 'ingredients':
                text = input('Ingredients is blank. Enter the ingredients for the recipe separated by commas.\n')
                entry = text.split(',')

            # Set remaining fields with generic message
            else:
                entry = input(f'{field.title()} is blank. Enter the {field} for the recipe.\n')
            new_recipe[field] = entry

    # Add recipie to master list
    recipes.append(new_recipe)

    # Pickle new recipie list
    support.save_obj(recipes, 'recipes')

    # Reset screen
    support.screen_reset()

    # Retry Check
    # If true, retry URL used to recursivly call function, flag prevents extra add again checks
    if rec_retry == True:
        return None

    # Add another recipie check
    add_again = input('Would you like to add another recipe? (y/n): ')
    while add_again.lower() not in ['y', 'n']:
        add_again = input('Would you like to add another recipe? (y/n): ')

    if add_again.lower() == 'y':
        add_recipe(recipes)


def find_recipe(recipes):
    search_fields = [
        {'name': 'Name', 'term': 'none'},
        {'name': 'Ingredients', 'term': 'none'},
    ]

    end_message = 'Undefined error.'

    # Reset screen
    support.screen_reset()

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
        support.screen_reset()

        # Randomly select recipe option
        recipe_option = random.choice(eligible_recipies)

        # Remove option from eligible recipes
        eligible_recipies.remove(recipe_option)

        # Display option
        support.display_recipe(recipe_option)

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
            support.screen_reset()
            # No more recipes message
            end_message = 'No other eligible recipes.'
            match_review = False
            break

    # Reset screen
    support.screen_reset()

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
