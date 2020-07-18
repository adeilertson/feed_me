import pickle

with open('C:/Users/adeil_000/Desktop/python_work/Games and Other Projects/Feed Me/data/web_recipe_schemeas.csv'):
    print('open')

with open(f'C:/Users/adeil_000/Desktop/python_work/Games and Other Projects/Feed Me/data/recipes.pkl', 'rb') as file:
    data = pickle.load(file)
