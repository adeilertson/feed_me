import csv
import pickle
import os

from feed_me_refs import known_sources


def save_obj(obj, filename):
    with open(f'C:/Users/adeil_000/Desktop/python_work/Games and Other Projects/Feed Me/data/{filename}.pkl', 'wb') as file:
        pickle.dump(obj, file)


def load_obj(filename):
    with open(f'C:/Users/adeil_000/Desktop/python_work/Games and Other Projects/Feed Me/data/{filename}.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


def import_recipes():
    with open(f'C:/Users/adeil_000/Desktop/python_work/Games and Other Projects/Feed Me/data/recipes.pkl', 'rb') as file:
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
    print(f"""
{recipe['name']}
Author - {recipe['chef']}
Yeild - {recipe['yeild']}

Ingredients:
{[step for step in recipe['instructions']]}
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
        fieldnames = recipes[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='Missing')
        for recipe in recipes:
            writer.writerow(recipe)
