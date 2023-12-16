"""
A simple recipie finder and manager.

Allows you to find a recipe from an intial set and add your own either manually
or through a URL. URLs from several popular recipe sites are processed to
identify recipie information, with missing information added manually
"""

import support
import actions
import screens
import models
import db_actions

def main():
    # Get recipes
    recipes = support.import_recipes()

    # Task options
    task_options = ['q', 'find', 'add', 'admin', 'test', 'search']
    admin_task_options = ['reset', 'remove']

    # Main Loop
    running = True
    while running is True:
        # Screen reset
        screens.screen_reset()

        # Print main menu
        screens.print_menu()

        # Get user command
        cmd = input('Enter command: ').lower()
        # Set/Reset result to blank
        res = '' 

        # Vailid command check
        if cmd not in task_options:
            res = input("Unknown command \n Press enter to continue.").lower()

        # Find a Recipe
        elif cmd == 'find':
            #actions.find_recipe(recipes)
            db_actions.db_test_query()
            res = input()

        elif cmd == 'search':
            db_actions.test_search('apple')
            res = input()

        # Add a Recipe
        elif cmd == 'add':
            #actions.add_recipe(recipes)
            db_actions.db_test_add()
            res = input()

        # Test db connection
        elif cmd == 'test':
            msg = db_actions.test_db_connection()
            print(msg)
            res = input()

        # Admin
        elif cmd == 'admin':
            admin_running = True
            while admin_running is True:
                # CLear screen and show admin menu
                screens.screen_reset()
                screens.print_admin_menu()

                # Admin command
                admin_cmd = input('Enter command: ')

                # Remove recipie
                if admin_cmd not in admin_task_options:
                    res = input("Unknown command \n Press enter to continue.").lower()
                elif admin_cmd == 'remove':
                    actions.delete_recipie()
                elif admin_cmd == 'reset':
                    actions.reset_recipie_table()

        # Exit check
        if cmd == 'q' or res == 'q':
            print('Exiting')
            running = False
            break


if __name__ == '__main__':
    main()
