"""
Database Actions


"""
from sqlalchemy import and_, or_, create_engine, MetaData, Table, select
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, contains_eager, joinedload
from sqlalchemy.exc import NoSuchTableError

import file_handling
import models


def test_db_connection():
    # Get config
    cfg = file_handling.get_cfg()

    # Connect to db
    engine = create_engine(cfg['database_path'])

    # Confirm connection
    with engine.connect() as connection:
        # Attempt to connect to recipes table to confirm connection
        meta = MetaData()
        try:
            recipe_table = Table('Recipe', meta, autoload_with=connection)
            result = f"Successfully connected to {cfg['database_path']}"
        except NoSuchTableError:
            result = f"Unable to connect to 'Recipe' table. Ensure database and table exists at {cfg['database_path']}"

    return result


def add_recipe(new_recipe):
    """
    Adds a provided recipe to the database.

    Adds recipe and ingridents to the database

    Args:
        new_recipe (list): List with recipe data
    """
    # Start session
    session = get_session()

    # Build recipe data model object
    recipe = models.Recipe(
        recipe_name=new_recipe['name'],
        chef=new_recipe['chef'],
        servings=new_recipe['yield'],
        url=new_recipe['url'],
        instructions=new_recipe['instructions'],
    )

    # Build ingrident data model objects
    ingredient_objects = [models.Ingredient(ingredient_name=ingredient) for ingredient in new_recipe['ingredients']]
    # Add ingridents to recipie
    recipe.ingredients = ingredient_objects
    # Add recipie object
    session.add(recipe)
    # Add ingrident object list
    session.add_all(ingredient_objects)
    # Commit to update database
    session.commit()

    # Close the session
    session.close()


def recipes_delete(recipe):
    pass


def db_reset():
    pass


def get_session():
    """
    Start session for database defined by 'database_path' in config file.

    Config location - feed_me/config/config.yml

    Returns:
        sqlalchemy.orm.Session: SQLAlchemy session with the config database
    """
    # Get config
    cfg = file_handling.get_cfg()

    # Connect to db
    engine = create_engine(cfg['database_path'])

    # Start session
    Session = sessionmaker(bind=engine)
    session = Session()

    return(session)


def run_ingredient_query(search_terms):
    """
    Search for recipes containing specified ingredients.

    Args:
        search_terms (list): A list of ingredient names to search for.

    Returns:
        list: A list of Recipe objects matching the criteria.
    """
    with get_session() as session:
        # Initialize an empty set to store lists of matching ingredient_ids
        matching_ingredient_lists = list()
    
        # Find matching ingredient_ids for each search term
        for term in search_terms:
            matching_ingredient_ids = (
                session.query(models.ingredient_association.c.ingredient_id)
                .join(models.Ingredient)
                .filter(models.Ingredient.ingredient_name.ilike(f'%{term}%'))
                .distinct()
                .all()
            )
    
            # Extract the ingredient_ids from the result and convert to a list
            matching_ingredient_ids = [ingredient_id for (ingredient_id,) in matching_ingredient_ids]
    
            # Add the list of ingredient_ids to the set
            matching_ingredient_lists.append(matching_ingredient_ids)
    
            # Sort list so search term with fewest matching IDs is first
            matching_ingredient_lists.sort(reverse=True)
    
            # Find recipes that have any ingredient matching the first search term
            query_recipes = (
                session.query(models.Recipe)
                .options(joinedload(models.Recipe.ingredients))  # Load all ingredients for recipes
                .join(models.ingredient_association)
                .filter(models.ingredient_association.c.ingredient_id.in_(matching_ingredient_lists[0]))
                .group_by(models.Recipe)
                .all()
            )
    
    # Filter initial set of recipes on the remaining matching ingredient lists
    
    recipes = []
    
    for recipe in query_recipes:
        # Get list of ingredient ids for recipe
        recipe_ingredient_ids = [ingredient.ingredient_id for ingredient in recipe.ingredients]
        # Check if recipe has at least one matching ingredient for each matching ingredients list
        for matching_list in matching_ingredient_lists[1:]:
            # Find instersection of two lists, where the lenght is the number ids in both lists, if zero, break the loop to go to next recipe
            if len(list(set(recipe_ingredient_ids) & set(matching_list))) == 0:
                break
        else:
            recipes.append(recipe)

    return recipes


def run_recipe_query(recipe_name):
    """
    Get a recipe by name and return it with all associated ingredients.

    Args:
        recipe_name (str): The name of the recipe to search for.

    Returns:
        models.Recipe or None: The Recipe object if found, otherwise None.
    """
    # Use a context manager to ensure proper session management
    with get_session() as session:
        # Build and run query
        recipe = (
            session.query(models.Recipe)
            .join(models.ingredient_association)
            .join(models.Ingredient)
            .filter(models.Recipe.recipe_name.ilike(f'%{recipe_name}%'))
            .options(contains_eager(models.Recipe.ingredients, alias=models.Ingredient))  # Eager-load all ingredients
            .first()
        )

    return recipe


def run_single_ingredient_query(search_terms):
    """
    Search for recipes containing specified ingredients.

    Args:
        search_terms (list): A list of ingredient names to search for.

    Returns:
        list: A list of Recipe objects matching the criteria.
    """
    # Start session for the query
    with get_session() as session:
        # Build and run query
        recipes = (
            session.query(models.Recipe)
            .join(models.ingredient_association)
            .join(models.Ingredient)
            .options(joinedload(models.Recipe.ingredients))  # Load all ingredients for recipes
            .filter(or_(*[models.Ingredient.ingredient_name.ilike(f'%{term}%') for term in search_terms])) # Filter on search terms where an ingredient contains at least one search term
            .group_by(models.Recipe.recipe_id)
            .all()
        )


    return recipes
