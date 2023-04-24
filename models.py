from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, Table, String, Boolean, Text, DateTime
from sqlalchemy import ARRAY
from sqlalchemy.orm import declarative_base, relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Users Table Model
class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(100), nullable=False)
    savedRecipes = relationship("savedUserRecipes", backref='savedUserRecipes', cascade='all, delete')
    shoppingList = relationship("shoppingList", backref='shoppingList', cascade='all, delete')
    is_Admin = Column(Boolean, nullable=False, default=False)
    dateCreated = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        template = '{0.id} {0.username} {0.savedRecipes} {0.email} {0.shoppingList} {0.is_Admin} {0.dateCreated}'
        return template.format(self)

# Recipes Table Model
class Recipes(db.Model):
    __tablename__= "Recipes"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    imageURL = Column(String(300), nullable=True)
    videoURL = Column(String(300), nullable=True)
    category = Column(String(50), nullable=True)
    prepTime = Column(String(50), nullable=True)
    cookTime = Column(String(50), nullable=True)
    servings = Column(String(50), nullable=True)
    ingredients = relationship("Ingredients", backref='recipe', cascade='all, delete-orphan')
    reviews = relationship("Reviews", backref='recipe', cascade='all, delete-orphan')
    ratingAvg = Column(String(10), nullable=True)
    ratingCount = Column(String(10), nullable=True)
    nutrition = relationship("Nutrition", backref='recipe', cascade='all, delete-orphan')
    dateCreated = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        template = '{0.id} {0.title} {0.category}'
        return template.format(self)


# Ingredients Table Model
class Ingredients(db.Model):
    __tablename__= "Ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    unit = Column(String(50), nullable=True)
    amount = Column(String(100), nullable=True)
    recipe_id = Column(Integer, ForeignKey("Recipes.id"))
    
    def __repr__(self):
        template = '{0.id} {0.name}'
        return template.format(self)
    
    
class Nutrition(db.Model):
    __tablename__= "Nutrition"
    id = Column(Integer, primary_key=True)
    calories = Column(String(100), nullable=True)
    carbohydrate = Column(String(100), nullable=True)
    cholesterol = Column(String(100), nullable=True)
    fiber = Column(String(100), nullable=True)
    protein = Column(String(100), nullable=True)
    saturatedFat = Column(String(100), nullable=True)
    sodium = Column(String(100), nullable=True)
    sugar = Column(String(100), nullable=True)
    fat = Column(String(100), nullable=True)
    unsaturatedFat = Column(String(100), nullable=True)
    recipe_id = Column(Integer, ForeignKey("Recipes.id"))
    
    def __repr__(self):
        template = '{0.id} {0.calories}'
        return template.format(self)
    
    
class Reviews(db.Model):
    __tablename__= "Reviews"
    id = Column(Integer, primary_key=True)
    author = Column(String(50), nullable=True)
    rating = Column(String(2), nullable=True)
    body = Column(String(300), nullable=True)
    recipe_id = Column(Integer, ForeignKey("Recipes.id"))
    
    def __repr__(self):
        template = '{0.id} {0.author} {0.rating} {0.body} {0.recipe_id}'
        return template.format(self)
    
    
class shoppingList(db.Model):
    __tablename__ = "shoppingList"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    ingredient = Column(String(100), nullable=False)
    
    def __repr__(self):
        template = '{0.ingredient}'
        return template.format(self)
    
    
# SavedRecipes Table Model
class savedUserRecipes(db.Model):
    __tablename__= "savedUserRecipes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    recipe_id = Column(Integer)
    
    def __repr__(self):
        template = '{0.id} {0.user_id} {0.recipe_id}'
        return template.format(self)
    
    