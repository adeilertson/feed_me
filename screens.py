"""
Screen printing functionn

@author: Andrew Eilertson
"""

import os


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


def print_menu():
    print("""
        Welcome to Feed Me!

        Your recipie picking solution for when no one knows what they want!

        Options:
        - 'find' to search for a recipe
        - 'add' to add a new recipie to the repository
        - 'q' to exit
        """)


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
