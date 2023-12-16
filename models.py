"""
Feed Me Data Models


"""
from __future__ import annotations
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import file_handling

# Create database engine
cfg = file_handling.get_cfg()
engine = create_engine(cfg['database_path'])

# Create database session
# Session = sessionmaker(bind=engine)
# session = Session()


Base = declarative_base()


# Ingrediant and Recipe Association table
# class IngredientAsociation(Base):
#     """Association model for Ingredients and Recipes"""
#     __tablename__ = 'IngredientAssociation'

#     # Set table fields
#     asscociation_id = Column(Integer, primary_key=True, autoincrement=True)
#     recipe_id = Column(Integer, ForeignKey('Recipe.recipe_id'))
#     ingredient_id = Column(Integer, ForeignKey('Ingredient.ingredient_id'))

# IngredientAsociation = Table(
#     'ingredient_association',
#     Base.metadata,
#     Column('asscociation_id', Integer, primary_key=True),
#     Column('recipe_id', Integer, ForeignKey('Recpie.recipe_id')),
#     Column('ingredient_id', Integer, ForeignKey('Ingredient.ingredient_id'))
#     )

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
    #ingredients: Mapped[list[Ingredient]] = relationship(secondary=ingredient_association, back_populates="recipes")
    ingredients = relationship("Ingredient", secondary=ingredient_association, back_populates="recipes")

    def __repr__(self):
        return f"Recipe {self.name}"


# Ingredient data model
class Ingredient(Base):
    """Ingredient entry"""

    __tablename__ = 'Ingredient'

    # Set table fields
    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_name = Column(String(255))
    #recipes: Mapped[list[Recipe]] = relationship(secondary=ingredient_association, back_populates='ingredients')
    recipes = relationship("Recipe", secondary=ingredient_association, back_populates='ingredients')


Base.metadata.create_all(engine)
