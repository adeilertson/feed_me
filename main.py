"""
A simple recipie finder and manager.

Allows you to find a recipe from an intial set and add your own either manually
or through a URL. URLs from several popular recipe sites are processed to
identify recipie information, with missing information added manually
"""
import actions
import screens
import models
import db_actions
import file_handling

def main():
    # Check if database exists
    res = db_actions.test_db_connection()
    if "Successfully connected" not in res:
        cfg = file_handling.get_cfg()
        print(f"Unable to connect to database at {cfg['database_path']}")
        create_check = input(f"\n\nCreate database at path above? (y/n) ").lower()
        if create_check == 'y':
            models.initialize_database()
            res = db_actions.test_db_connection()
            if "Successfully connected" not in res:
                print(f"Unable to connect to database at {cfg['database_path']}")
                cont = input("\nUnknown issue preventing databse creation/connection. Press enter to exit.")
                return None
            else:
                cont = input(f"\nDatabase created. Press enter to go to main menu.")
        else:
            return None

    # Task options
    task_options = ['q', 'find', 'search', 'browse', 'add', 'test']

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

        # Find recipe by name
        elif cmd == 'find':
            actions.find_recipe()

        # Search for recipes with an ingredient
        elif cmd == 'search':
            actions.ingredient_search()

        # Browse all recipes
        elif cmd == 'browse':
            actions.browse_recipes()

        # Add a Recipe
        elif cmd == 'add':
            actions.add_recipe()

        # Test db connection
        elif cmd == 'test':
            msg = db_actions.test_db_connection()
            print(msg)
            res = input()

        # Exit check
        if cmd == 'q' or res == 'q':
            print('Exiting')
            running = False
            break


if __name__ == '__main__':
    main()
