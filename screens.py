"""
Screen printing functionn

@author: Andrew Eilertson
"""
import os


def display_recipe(recipe):
    # Set ingredients to string
    ingredients = '\n'.join(recipe['ingredients']).title()
    # Print the recipe
    print(f"""
{recipe['name']}
Author - {recipe['chef']}
Yield - {recipe['yield']}
URL - {recipe['url']}

Ingredients:

{ingredients}

Instructions:
{recipe['instructions']}
    """)


def print_ingredient_search_instructions():
    print("""
Enter each ingrident to search for and then press 'Enter'.
After you're done adding ingredients, press 'Enter' again.

    """)


def print_menu():
    print("""
        Welcome to Feed Me!

        Your recipie picking solution for when no one knows what they want!

        Options:
        - 'search' to search for a recipe based on ingredients 
        - 'add' to add a new recipie to the repository
        - 'admin' to manage the recipies database
        - 'q' to exit
        """)
    

def print_admin_menu():
    print("""
        Feed Me Database Admin Menu

        Options:
        - 'remove' to remove a recipie from the database by name
        - 'reset' to reset the recipie table, deleting all stored recipie data
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
