

from feed_me_support import (
    import_recipes,
    screen_reset,
)

from feed_me_core_fuctions import (
    find_recipe,
    add_recipe
)

# Get recipes
recipes = import_recipes()

# Task options
task_options = ['q', 'find', 'add']

# Main Loop
running = True
while running is True:
    # Screen reset
    screen_reset()

    # Print main menu
    print("""
Welcome to Feed Me!

Your recipie picking solution for when no one knows what they want!

Enter 'find' to search for a recipe
Enter 'add' to add a new recipie to the repository
Enter 'q' to exit
    """)

    # User enter desired option
    task = input('Enter selection: ').lower()
    # Task selection loop
    if task not in task_options:
        task = input('Invalid entry. Re-Enter selection: ')

    # Exit
    if task == 'q':
        print('Exiting')
        running = False
        break

    # Find a Recipe
    if task == 'find':
        find_recipe(recipes)

    # Add a Recipe
    if task == 'add':
        add_recipe(recipes)
