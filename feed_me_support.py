"""
Support functions for Feed Me.

@author: Andrew Eilertson

Created: 7/17/2020
Updated: 7/20/2021
"""

import csv
import pickle
import os

from feed_me_refs import known_sources


def save_obj(obj, filename):
    with open(f'C:/Users/adeil/Desktop/python/feed_me/data/{filename}.pkl', 'wb') as file:
        pickle.dump(obj, file)


def load_obj(filename):
    with open(f'C:/Users/adeil/Desktop/python/feed_me/data/{filename}.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


def import_recipes():
    with open(f'C:/Users/adeil/Desktop/python/feed_me/data/recipes.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


def screen_reset():
    # Clear screen
    os.system('cls')
    # Print header
    print("""
    ______              __   __  ___     __
   / ____/__  ___  ____/ /  /  |/  /__  / /
  / /_  / _ \/ _ \/ __  /  / /|_/ / _ \/ / 
 / __/ /  __/  __/ /_/ /  / /  / /  __/_/  
/_/    \___/\___/\__,_/  /_/  /_/\___(_)   
    """)


def recipe_source(url):
    """Determine if URL is from known source. Returns source or 'unkown'"""

    # Get base url
    base_url = url.split('/')[2]

    # Check if base url in known sources
    if base_url in known_sources.keys():
        source = known_sources[base_url]
    else:
        source = 'unknown'

    return(source)


def display_recipe(recipe):
    # Set ingredients to string
    ingredients = '\n'.join(recipe['ingredients']).title()
    # Set instructions to string
    instructions = ''
    for num, step in enumerate(recipe['instructions'], start=1):
        instructions += f'\n{num}. {step}'
    # Print the recipe
    print(f"""
{recipe['name']}
Author - {recipe['chef']}
Yeild - {recipe['yeild']}
URL - {recipe['url']}

Ingredients:

{ingredients}

Instructions:
{instructions}
    """)


def set_instructions(instr):
    # Set blank list for instruction entries
    inst_list = []
    # Cycle through each entry in web instruction
    for entry in instr:
        # Add text value to instruction list
        inst_list.append(entry['text'])
    # Return list of instructions
    return inst_list


def write_cookbook(recipes):
    # Wrtie entire recipe set to csv file

    # Default output file to current directory
    filename = 'cookbook.csv'
    with open(filename, 'w', newline='') as f:
        fieldnames = recipes[-1].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='Missing', extrasaction='ignore')
        for recipe in recipes:
            writer.writerow(recipe)

def add_csv_recipes(file, replace_all=False):
    if replace_all is False:
        # Load main recipe list
        recipes = import_recipes()
    elif replace_all is True:
        recipes = []
    with open(file) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            new_recipe = {
                'error': '',
                'name': row[0],
                'url': row[1],
                'ingredients': row[2],
                'yeild': row[3],
                'instructions': row[4],
                'chef': row[5],
                'cuisine': row[6],
                'method': row[7],
                'season': row[8],
                'dish': row[9],
            }

            # Add recipie to main list
            recipes.append(new_recipe)

    # Pickle new recipie list
    save_obj(recipes, 'recipes')
