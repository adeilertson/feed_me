from feed_me_support import (
    import_recipes,
    save_obj
)

# Get recipes
recipes = import_recipes()

# Check if each standard key is in each recipe
for recipe in recipes:
    if 'name' not in recipe.keys():
        recipe['name'] = ''
    if 'cuisine' not in recipe.keys():
        recipe['cuisine'] = ''
    if 'method' not in recipe.keys():
        recipe['method'] = ''
    if 'dish' not in recipe.keys():
        recipe['dish'] = ''
    if 'season' not in recipe.keys():
        recipe['season'] = ''
    if 'chef' not in recipe.keys():
        recipe['chef'] = ''
    if 'yeild' not in recipe.keys():
        recipe['yeild'] = 0
    if 'url' not in recipe.keys():
        recipe['url'] = ''
    if 'ingredients' not in recipe.keys():
        recipe['ingredients'] = []
    if 'instructions' not in recipe.keys():
        recipe['instructions'] = []

# Pickle revised recipe list
save_obj(recipes, 'recipes')
