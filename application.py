from flask import Flask, render_template, request, redirect, jsonify, Markup, url_for, flash, session, Blueprint
from flask_login import LoginManager, login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor
from flask_cdn import CDN
import os, json, pymysql, chardet, util, requests
from models import *
from quicktype.recipeType import recipe_from_dict, recipe_to_dict
from ingredient_parser import parse_ingredient
from config import Config
import random

application = Flask(__name__)
application.config.from_object(Config)

# If application detects rds database, use cloud database, if not use localhost
if 'RDS_HOSTNAME' in os.environ:
    CDN(application)

    
db.init_app(application)
migrate.init_app(application, db)
ckeditor = CKEditor(application)

# Init Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# blueprint for auth routes in our application
from auth import auth as auth_blueprint
application.register_blueprint(auth_blueprint)


@application.route("/")
def index():
    # util.populate()    # Uncomment this line to populate database with test data.
    url = Config.API_URL + '/recipes'
    response = requests.get(url)
    if response.status_code == 404:
        recipes = "No Recipes Found"
        flash("No Recipes Found", 404)
    elif response.status_code == 100:
        recipes = "Incorrect Query"
        flash("Incorrect Query", 100)
    else:
        recipes = response.json()
        return render_template("index.html", recipes=recipes, name="Ecochef", user=current_user)
    print(recipes)
    return render_template("index.html", name="Ecochef", user=current_user)
    
    
@application.route("/search", methods=["POST", "GET"])
def search():
    url = Config.API_URL + '/recipes'
    response = requests.get(url)
    if response.status_code == 404:
        recipes = "No Recipes Found"
        flash("No Recipes Found", 404)
    elif response.status_code == 100:
        recipes = "Incorrect Query"
        flash("Incorrect Query", 100)
    else:
        recipes = response.json()
        return render_template("search.html", recipes=recipes, name="Ecochef", user=current_user)
    print(recipes)
    return render_template("search.html", name="Ecochef", user=current_user)


@application.route("/recipe/<id>", methods=["GET"])
def recipe(id):
    url = Config.API_URL + '/recipe/' + id
    response = requests.get(url)
    if response.status_code == 404:
        recipe = "No Recipes Found"
        flash("No Recipes Found", 404)
    elif response.status_code == 100:
        recipe = "Incorrect Query"
        flash("Incorrect Query", 100)
    else:
        recipe = response.json()
        
        ingredientIDs = []
        for ingredient in recipe['ingredients']:
            ingredientIDs.append(ingredient['id'])
        
        recipeReviews = recipe['reviews']
        reviews = random.choices(recipeReviews, k=5)
        
        return render_template("recipe.html", recipe=recipe, ingredients=ingredientIDs, reviews=reviews, name="Ecochef", user=current_user)
    print(recipe)
    return render_template("recipe.html", name="Ecochef", user=current_user)

@application.route("/favourites")
@login_required
def favourites():
    savedRecipes = current_user.savedRecipes
    print(savedRecipes)
    return render_template('savedRecipes.html', recipes=savedRecipes, user=current_user, name="Ecochef")


@application.route("/saveRecipe/<id>")
@login_required
def saveRecipe(id):
    user = Users.query.filter_by(id=current_user.id).first()
    saveRecipe = savedUserRecipes(userID=user.id, RecipeID=id)
    checkIfExists = savedUserRecipes.query.filter_by(userID=user.id, RecipeID=saveRecipe.RecipeID).first()
    if checkIfExists:
        flash('Recipe Already Saved')
        print(checkIfExists)
    else:
        user.savedRecipes.append(saveRecipe)
        db.session.commit()
        flash('Recipe Saved')
    return redirect(url_for('showRecipe', id=id))








@application.route("/createRecipe", methods=["POST", "GET"])
@login_required
def createRecipe():
    url = Config.API_URL + '/recipe'
    
    if request.method == "POST":
        # store values recieved from HTML form in local variables
        title=request.form.get("title")
        instructions=request.form.get("ckeditor")
        category=request.form.get("category")
        servings=request.form.get("servings")
        prepTime=request.form.get("prepTime")
        cookTime=request.form.get("cookTime")
        count=request.form.get("count")
        imageURLforDB='img/recipeImages/default.jpg'
        
        # Image Handling
        if 'recipeImage' not in request.files:
            print("No file part")
        file=request.files['recipeImage']
        if file.filename == '':
            print("No selected file")
        if file and util.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            imageURL = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            imageURLforDB = os.path.join('img/recipeImages/', filename)
            file.save(imageURL)
        
        # Creating Recipe Object
        recipe = Recipes(title=title,
                            instructions=instructions,
                            category=category,
                            imageURL=imageURLforDB,
                            servings=servings,
                            prepTime=prepTime,
                            cookTime=cookTime)
        
        # Populating Recipe with user submitted ingredients
        for x in range(int(count)):
            ingredientIdentifier = 'ingredient-' + str(x+1)
            ingredientName = request.form.get(ingredientIdentifier)
            ingredient = Ingredients(name=ingredientName)
            recipe.ingredients.append(ingredient)

        payload = json.dumps(recipe.format())
        headers = {
        'x-access-token': current_user.api_token,
        'Content-Type': 'application/json',
        'Authorization': 'Basic QWRtaW46MTIzNDU='
        }

        response = requests.post(url, headers=headers, data=payload)

        print(response.text)
        # Adding and commiting new recipe to database
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe Created.', 200)
        return redirect(url_for('index'))
    return render_template("createRecipe.html", name="Ecochef", user=current_user)


@application.route("/showRecipe/<id>")
def showRecipe(id):
    recipe=Recipes.query.filter_by(id=id).one()
    methodMarkup = recipe.instructions
    ingredientIDs = []
    for ingredient in recipe.ingredients:
        ingredientIDs.append(ingredient.id)
        
    return render_template("showRecipe.html", recipe=recipe, ingredientIDs=ingredientIDs, method=methodMarkup, name="Ecochef", user=current_user)


@application.route("/deleteRecipe/<id>")
@login_required
def deleteRecipe(id):
    recipe = Recipes.query.filter_by(id=id).one()
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe Deleted')
    
    util.logThis("deleted", current_user.username, current_user.id, recipe.title, recipe.id)
    return redirect(url_for('index'))


@application.route("/profile")
@login_required
def profile():
    url = Config.API_URL + "/user/" + str(current_user.id)
    token = util.get_token(current_user)
    payload = {}
    headers = {
    'x-access-token': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    url = Config.API_URL + "/users"
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json().users)
    users = response.json()
    logs = []
    for line in reversed(list(open("log.txt"))):
        logs.append(line.rstrip())

    savedRecipes = current_user.savedRecipes
    userRecipes = []
    for recipe in savedRecipes:
        recipe = db.session.query(Recipes).filter_by(id = recipe.RecipeID).all()
        userRecipes += recipe
        
    shoppinglist = current_user.shoppingList
    
    return render_template('profile.html', user=current_user, logs=logs, shopping_list=shoppinglist, user_recipes=userRecipes, user_list=users, skip=skip, name="Ecochef")


@application.route("/makeAdmin/<id>")
@login_required
def makeAdmin(id):
    if current_user.is_Admin:
        user = Users.query.filter_by(id=id).first()
        print(user)
        user.is_Admin = True
        db.session.commit()
        util.logThis("Made Admin", current_user.username, current_user.id, user.username, user.id)
        flash(user.username + ' is now an Admin')
    else:
        flash('You need to be admin to do that!')
    return redirect(url_for('profile'))


@application.route("/revokeAdmin/<id>")
@login_required
def revokeAdmin(id):
    if current_user.is_Admin:
        user = Users.query.filter_by(id=id).first()
        print(user)
        user.is_Admin = False
        db.session.commit()
        util.logThis("Revoked Admin", current_user.username, current_user.id, user.username, user.id)
        flash(user.username + ' is no longer an Admin')
    else:
        flash('You need to be admin to do that!')
    return redirect(url_for('profile'))


@application.route("/saveRecipe/<id>")
@login_required
def saveRecipe(id):
    user = Users.query.filter_by(id=current_user.id).first()
    saveRecipe = savedUserRecipes(userID=user.id, RecipeID=id)
    checkIfExists = savedUserRecipes.query.filter_by(userID=user.id, RecipeID=saveRecipe.RecipeID).first()
    if checkIfExists:
        flash('Recipe Already Saved')
        print(checkIfExists)
    else:
        user.savedRecipes.append(saveRecipe)
        db.session.commit()
        flash('Recipe Saved')
    return redirect(url_for('showRecipe', id=id))

@application.route("/unsaveRecipe/<id>")
@login_required
def unsaveRecipe(id):
    user = Users.query.filter_by(id=current_user.id).first()
    unsaveRecipe = savedUserRecipes.query.filter_by(userID=user.id, RecipeID=id).first()
    if not unsaveRecipe:
        flash('Recipe Not Saved')
        print(unsaveRecipe)
    else:
        user.savedRecipes.remove(unsaveRecipe)
        db.session.commit()
        recipe = Recipes.query.filter_by(id=unsaveRecipe.RecipeID).first()
        flashmsg = 'Removed ' + recipe.title + ' from saved recipes.'
        flash(flashmsg)
    return redirect(url_for('profile'))

    
@application.route("/savedRecipes")
@login_required
def savedRecipes():
    savedRecipes = current_user.savedRecipes
    recipes = []
    for recipe in savedRecipes:
        recipe = db.session.query(Recipes).filter_by(id = recipe.RecipeID).all()
        recipes += recipe
    return render_template('savedRecipes.html', recipes=recipes, user=current_user, name="Ecochef")


@application.route("/editRecipe/<id>", methods=["POST", "GET"])
@login_required
def editRecipe(id):
    recipe = Recipes.query.filter_by(id=id).first()
    if request.method == "POST":
        # store values recieved from HTML form in local variables
        recipe.title=request.form.get("title")
        recipe.method=request.form.get("ckeditor")
        recipe.category=request.form.get("category")
        recipe.servings=request.form.get("servings")
        recipe.prepTime=request.form.get("prepTime")
        recipe.cookTime=request.form.get("cookTime")
        count=request.form.get("count")
        
        if 'recipeImage' not in request.files:
            print("No file part")
        file=request.files['recipeImage']
        if file.filename == '':
            print("No selected file")
        if file and util.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            imageURL = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            imageURLforDB = os.path.join('img/recipeImages/', filename)
            recipe.imageURL = imageURLforDB
            file.save(imageURL)
    
        for x in range(int(count)):
            ingredientIdentifier = 'ingredient-' + str(x+1)
            ingredientName = request.form.get(ingredientIdentifier)
            ingredient = Ingredients(name=ingredientName)
            checkIngredients = Ingredients.query.filter_by(name=ingredient.name).all()
            if checkIngredients:
                
                for checkIngredient in checkIngredients:
                    print(checkIngredient)
                    if checkIngredient == ingredient.name:
                        recipe.ingredients.remove(ingredient)
                    print('Ingredient Already Exists')
            else:
                recipe.ingredients.append(ingredient)

        db.session.commit()
        flash('Recipe Edited.')
        return redirect(url_for('showRecipe', id=id))
    return render_template('editRecipe.html', recipe=recipe, user=current_user, name="Ecochef")


@application.route("/addToShoppingList/<ingredientIDs>")
@login_required
def addToShoppingList(ingredientIDs):
    user = Users.query.filter_by(id=current_user.id).first()
    
    
    strippedString = ingredientIDs.lstrip("[").rstrip("]")
    ingredients = strippedString.split(', ')
    
    def exists(ingredient):
        for shoppingList in user.shoppingList:
            if shoppingList.ingredient == ingredient.name:
                return True
        return False
        
    for ingredientID in ingredients:
        ingredient = Ingredients.query.filter_by(ingredient_id=ingredientID).one()
        if exists(ingredient):
            print('already exists')
        else:
            print('adding item')
            shoppingListItem = shoppingList(ingredient=ingredient.name)
            user.shoppingList.append(shoppingListItem)
    
    flash('Ingredients added to shopping list')
    db.session.commit()
    return redirect(url_for('showShoppingList'))


@application.route("/removeFromShoppingList/<id>")
@login_required
def removeFromShoppingList(id):
    user = Users.query.filter_by(id=current_user.id).first()
    shoppingListItem = shoppingList.query.filter_by(id=id).first()
    if shoppingListItem:
        user.shoppingList.remove(shoppingListItem)
        db.session.commit()
        flashmsg = 'Removed ' + shoppingListItem.ingredient + ' from shopping list'
        flash(flashmsg)
    else:
        flashmsg = 'Ingredient not Found'
        flash(flashmsg)
    return redirect(url_for('showShoppingList'))


@application.route("/shoppingList")
@login_required
def showShoppingList():
    shoppingList = current_user.shoppingList
    print(shoppingList)
    return render_template('shoppingList.html', user=current_user, shoppingList=shoppingList, name="Ecochef")


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    



  