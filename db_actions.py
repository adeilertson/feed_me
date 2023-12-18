import pprint as pp

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload

import file_handling
import models


def test_db_connection():
    # Get config
    cfg = file_handling.get_cfg()

    # Set default result
    result = f"Unable to connect to {cfg['database_path']}"

    # Connect to db
    engine = db.create_engine(cfg['database_path'])

    # Confirm connection
    with engine.connect() as connection:
        # Attempt to connect to recipes table to confirm connection
        meta = db.MetaData()
        recipe_table = db.Table('Recipe', meta, autoload_with=connection)
        result = f"Successfully connected to {cfg['database_path']}"

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
    # Get config
    cfg = file_handling.get_cfg()

    # Connect to db
    engine = db.create_engine(cfg['database_path'])

    # Delete data from db
    with engine.connect() as connection:
        meta = db.MetaData()
        recipe_table = db.Table('recipes', meta, autoload_with=connection)
        connection.execute(db.delete(recipe_table).where(recipe_table.c.name == recipe))
        connection.commit()


def db_reset():
    # Set Base
    Base = declarative_base()

    # Get cfg
    cfg = file_handling.get_cfg()

    # Connect to db
    engine = db.create_engine(cfg['database_path'])

    # Drop all tables
    Base.metadata.drop_all(engine)

    with engine.connect() as connection:

        Recipie = models.Recipie()
        Ingredient = models.Ingredient()
        IngredientAssociation = models.IngredientAsociation()
        Base.metadata.create_all(engine)

        print(f"Database reset {cfg['database_path']}")


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
    engine = db.create_engine(cfg['database_path'])

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
    # Start session for the query
    session = get_session()
    # Build and run query
    result = (
        session.query(models.Recipe)
        .join(models.ingredient_association)
        .join(models.Ingredient)
        .filter(db.and_(*[models.Ingredient.ingredient_name.ilike(f'%{term}%') for term in search_terms]))
        .group_by(models.Recipe.recipe_id)
        .all()
    )
    
    return result
