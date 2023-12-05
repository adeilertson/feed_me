import sqlalchemy as db

import file_handling


def test_db_connection():
    # Set default result
    result = result = f"Unable to connect to {cfg['database_path']}"

    # Get config
    cfg = file_handling.get_cfg()

    # Connect to db
    engine = db.create_engine(cfg['database_path'])

    # Confirm connection
    with engine.connect() as connection:
        # Attempt to connect to recipes table to confirm connection
        meta = db.MetaData()
        recipe_table = db.Table('recipes', meta, autoload_with=connection)
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


def recipes_reset():
    # Get cfg
    cfg = file_handling.get_cfg()

    # Connect to db
    engine = db.create_engine(cfg['database_path'])

    with engine.connect() as connection:
        # Drop recipe table
        try:
            meta = db.MetaData()
            recipe_table = db.Table('recipes', meta, autoload_with=connection)
            recipe_table.drop(connection)
            print(f"Recipes table dropped from {cfg['database_path']}")
        except db.exc.NoSuchTableError:
            print(f"Recipes table does not exist in {cfg['database_path']}")

        # Create new recipe table
        new_recipe_table = db.Table(
            'recipes',
            meta,
            db.Column('id', db.Integer, primary_key=True, autoincrement=True),
            db.Column('name', db.String),
            db.Column('add_date', db.Date),
            db.Column('error', db.String),
            db.Column('chef', db.String),
            db.Column('yeild', db.String),
            db.Column('url', db.String),
            db.Column('ingredients', db.String),
            db.Column('instructions', db.String),
        )

        meta.create_all(connection)
        connection.commit()
        print(f"Blank recipes tabled added to {cfg['database_path']}")
