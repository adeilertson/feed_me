import pprint as pp

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


def recipes_insert(new_recipe):
    # Get config
    cfg = file_handling.get_cfg()

    # Connect to db
    engine = db.create_engine(cfg['database_path'])

    # Add data to db
    with engine.connect() as connection:
        meta = db.MetaData()
        recipe_table = db.Table('recipes', meta, autoload_with=connection)
        connection.execute(db.insert(recipe_table), new_recipe)
        connection.commit()


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


def recipes_query():
    pass
    # SELECT CS.Recipie
    # FROM RecipieIngredients AS RI
    #     INNER JOIN
    #     QueryIngredients AS QI
    #         ON RI.Ingredients = QI.Ingridents
    # GROUP BY Recipie
    # HAVING COUNT(*) = ( SELECT COUNT(*)
    #                     FROM QueryIngredients
    #                     GROUP BY ());


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
    # Get config
    cfg = file_handling.get_cfg()

    # Connect to db
    engine = db.create_engine(cfg['database_path'])

    # Start session
    Session = sessionmaker(bind=engine)
    session = Session()

    return(session)


def test_search(search):
    session = get_session()
    # Query Ingredient table for specific ingredient
    query = session.query(models.Ingredient).where(models.Ingredient.ingredient_name==search).all()

    print(f"Recipes with {search}")
    for result in query:
        for recipe in result.recipes:
            print(recipe.recipe_name)


def db_test_query():
    session = get_session()
    records = session.query(models.Ingredient).filter_by(ingredient_name='apple').all()
    
    print(records[0].__dict__)

    # for rec in records:
    #     print(rec.__dict__)

    # records = session
    # .query(Customer)
    # .filter_by(first_name="Carl")
    # .all()

