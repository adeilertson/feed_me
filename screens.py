"""
Screen printing functionn

@author: Andrew Eilertson
"""
import os


def display_recipe(recipe):
    # Set ingredients to string
    ingredients_list = [ingredient.ingredient_name for ingredient in recipe.ingredients]
    ingredients = '\n'.join(ingredients_list).title()
    # Print the recipe
    print(f"""
{recipe.recipe_name}

Author - {recipe.chef}
Yield - {recipe.servings}
URL - {recipe.url}

Ingredients:

{ingredients}

Instructions:
{recipe.instructions}
    """)


def print_ingredient_search_instructions():
    print("""
Enter each ingrident to search for and then press 'Enter'.
After you're done adding ingredients, press 'Enter' again.

    """)


def print_find_recipe_instructions():
    print("""
Enter recipe name or text for the name to contain and press 'Enter'.
""")


def print_menu():
    print("""
        Welcome to Feed Me!

        Your recipie picking solution for when no one knows what they want!

        Options:
        - 'find' to find a recipe by name
        - 'search' to search for a recipe based on ingredients
        - 'browse' to look through all recipes
        - 'add' to add a new recipie to the repository
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
