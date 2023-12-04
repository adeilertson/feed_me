"""
A simple recipie finder and manager.

Allows you to find a recipe from an intial set and add your own either manually
or through a URL. URLs from several popular recipe sites are processed to
identify recipie information, with missing information added manually
"""

import feed_me_support
import feed_me_core_fuctions

def print_menu():
    print("""
        Welcome to Feed Me!

        Your recipie picking solution for when no one knows what they want!

        Enter 'find' to search for a recipe
        Enter 'add' to add a new recipie to the repository
        Enter 'q' to exit
        """)

def main():
    # Get recipes
    recipes = feed_me_support.import_recipes()

    # Task options
    task_options = ['q', 'find', 'add']

    # Main Loop
    running = True
    while running is True:
        # Screen reset
        feed_me_support.screen_reset()

        # Print main menu
        print_menu()

        # Get user command selection
        cmd = input('Enter selection: ').lower()
        # Set result to blank
        res = '' 

        # Vailid command check
        if cmd not in task_options:
            res = input("Unknown command \n Press enter to continue.").lower()
        # Find a Recipe
        elif cmd == 'find':
            feed_me_core_fuctions.find_recipe(recipes)

        # Add a Recipe
        elif cmd == 'add':
            feed_me_core_fuctions.add_recipe(recipes)
        # Exit check
        if cmd == 'q' or res == 'q':
            print('Exiting')
            running = False
            break
