# Feed Me
Version 0.1

## Description
A simple tool to find a recipe matching specific criteria, with the option to add new entries from a URL or manually, creating a personal database of recipes.

Key Aspects
- Terminal based user interface
- Many to many database structure for recipes and ingridents
- Automated recipe parsing from common websites
    - Delish
    - Bon Appetit
    - Food Network
    - Salt and Lavender
    - Macheesmo

## Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/adeilertson/feed_me
```

Change into the project directory:

```bash
cd feed_me
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
py main.py
```

When prompt appears, allow creation of data/feed_me.db

## Usage

### Populating the Database
You can add recipes with just a URL from sites that have a defined format to extract and parse the recipe data. If any fields are missing, you will be prompted to enter them.

You can also manually add recipes, entering each field yourself

### Finding Recipes by Ingredients
Feed Me! When you want to find recipes based on what you have, what's on sale, or what's in season. Enter a few ingredients and see recipes that make use of them. The more recipes you have, the better.

### Finding Recipes by Name
Simple serach to find recipe names that match/contain your search

### Browse
For when you don't have even have an ingreient or just can't find what you're looking for, you can see all the recipes in the database and then view and switch between them.

## Updates

## Future Features

- Additonal website collection options
- Search by Chef, Yield, or Instructions
- Add favorites