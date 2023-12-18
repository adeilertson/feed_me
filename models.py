"""
Feed Me Data Models


"""
from sqlalchemy import create_engine, Column, DateTime, ForeignKey, Integer, String, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import file_handling


Base = declarative_base()

ingredient_association = Table(
    "IngredientAssociation",
    Base.metadata,
    Column("recipe_id", ForeignKey("Recipe.recipe_id"), primary_key=True),
    Column("ingredient_id", ForeignKey("Ingredient.ingredient_id"), primary_key=True),
)


# Recipe data model
class Recipe(Base):
    """Recipe entry"""
    
    __tablename__ = 'Recipe'

    # Set table fields
    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_name = Column(String(255))
    chef = Column(String(255))
    servings = Column(String(255))
    url = Column(String(255))
    add_date = Column(DateTime, server_default=func.now())
    instructions = Column(Text)

    # Set table relationships - 
    ingredients = relationship("Ingredient", secondary=ingredient_association, back_populates="recipes")

    def __repr__(self):
        return f"Recipe {self.recipe_name}"


# Ingredient data model
class Ingredient(Base):
    """Ingredient entry"""

    __tablename__ = 'Ingredient'

    # Set table fields
    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_name = Column(String(255))
    recipes = relationship("Recipe", secondary=ingredient_association, back_populates='ingredients')


def initialize_database():
    """
    Create database with tables defined in feed_me/models located specified in config file as 'database_path'

    Config location - feed_me/config/config.yml
    """

    cfg = file_handling.get_cfg()
    engine = create_engine(cfg['database_path'])
    
    Base.metadata.create_all(engine)
