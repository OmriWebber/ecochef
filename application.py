from flask import Flask, render_template, request, redirect, jsonify, Markup, url_for, flash, session, Blueprint
from flask_login import LoginManager, login_required, current_user
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor
from flask_cdn import CDN
from functools import wraps
import os, json, pymysql, chardet, util, requests
from ingredient_parser import parse_ingredient
from config import Config
import random, jwt

application = Flask(__name__)
application.config.from_object(Config)

# If application detects rds database, use cloud database, if not use localhost
if 'RDS_HOSTNAME' in os.environ:
    CDN(application)
    
ckeditor = CKEditor(application)

# blueprint for auth routes in our application
from auth import auth as auth_blueprint
application.register_blueprint(auth_blueprint)


@application.route("/")
def index():
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
        categories = []
        for recipe in recipes['recipes']:
            if recipe['category'] not in categories:
                categories.append(recipe['category'])
        print(categories)
        if session.get('user') is not None:
            userURL = Config.API_URL + '/currentuser'
            headers = {
                'x-access-token': session['user']['token']
            }
            user = requests.get(userURL, headers=headers)
            if user.status_code == 401:
                flash("Session Expired", 401)
                return redirect(url_for('auth.logout'))
            print(user.json())
            JsonUser = user.json()['user']
            LikesList = []
            for likes in JsonUser['likes']:
                LikesList.append(likes)
            return render_template("index.html", recipes=recipes, likes=LikesList, name="Ecochef")
        return render_template("index.html", recipes=recipes, name="Ecochef")
    return render_template("index.html", recipes=recipes, likes=LikesList, name="Ecochef")
    
    
@application.route("/search", methods=["POST", "GET"])
def search():
    return render_template("search.html", name="Ecochef")
    

@application.route("/searchByIngredient", methods=["POST"])
def searchByIngredients():
    url = Config.API_URL + '/search/ingredients'
    ingredients = request.form.getlist('ingredient-name')
    payload = json.dumps({ "ingredients": ingredients })
    headers = { 'Content-Type': 'application/json' }
    response = requests.get(url, headers=headers, data=payload)
    if response.status_code == 404:
        results = "No Recipes Found"
        flash("No Recipes Found", 404)
    elif response.status_code == 100:
        results = "Incorrect Query"
        flash("Incorrect Query", 100)
    else:
        recipes = response.json()
        msg = "Found " + str(len(recipes)) + " recipes"
        flash(msg , 200)
        return render_template("results.html", recipes=recipes, name="Ecochef")
    return render_template("search.html", name="Ecochef", results=results)


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
        limit = 5
        if len(recipeReviews) < limit:
            limit = len(recipeReviews)
        reviews = random.choices(recipeReviews, k=limit)
        
        if session.get('user') is not None:
            userURL = Config.API_URL + '/currentuser'
            headers = {
                'x-access-token': session['user']['token']
            }
            user = requests.get(userURL, headers=headers)
            JsonUser = user.json()['user']
            LikesList = []
            for likes in JsonUser['likes']:
                LikesList.append(likes)
        
        return render_template("recipe.html", recipe=recipe, ingredients=ingredientIDs, likes=LikesList, reviews=reviews, name="Ecochef")
    print(recipe)
    return render_template("recipe.html", name="Ecochef")

@application.route("/favourites")
def favourites():
    url = Config.API_URL + '/user/favourites'
    headers = {
        'x-access-token': session['user']['token']
    }
    
    response = requests.get(url, headers=headers)
    favourites = response.json()
    
    userURL = Config.API_URL + '/currentuser'
    user = requests.get(userURL, headers=headers)
    JsonUser = user.json()['user']
    LikesList = []
    for likes in JsonUser['likes']:
        LikesList.append(likes)
    return render_template('savedRecipes.html', recipes=favourites, likes=LikesList, name="Ecochef")





@application.route("/profile")
def profile():
    url = Config.API_URL + '/currentuser'
    print(session['user'])

    headers = {
        'x-access-token': session['user']['token']
    }
    
    response = requests.get(url, headers=headers)
    print(response.json())
    user = response.json()['user']
    return render_template('profile.html', user=user, name="Ecochef")









@application.route("/createRecipe", methods=["POST", "GET"])
def createRecipe():
    url = Config.API_URL + '/createrecipe'
    
    if request.method == "POST":
        # store values recieved from HTML form in local variables
        title=request.form.get("title")
        instructions=request.form.get("ckeditor")
        category=request.form.get("category")
        servings=request.form.get("servings")
        prepTime=request.form.get("prepTime")
        cookTime=request.form.get("cookTime")
        count=request.form.get("count")
        imageURLforDB='img/default.jpg'
        
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
        'x-access-token': session['user'].token,
        'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        print(response.text)
        # Adding and commiting new recipe to database
        flash('Recipe Created.', 200)
        return redirect(url_for('index'))
    return render_template("createRecipe.html", name="Ecochef")



@application.route("/editRecipe/<id>", methods=["POST", "GET"])
def editRecipe(id):
    url = Config.API_URL + '/recipe/' + id
    response = requests.get(url)
    if response.status_code == 404:
        recipe = "No Recipe Found"
        flash("No Recipes Found", 404)
    elif response.status_code == 100:
        recipe = "Incorrect Query"
        flash("Incorrect Query", 100)
    else:
        recipe = response.json()
        print(recipe)

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
                    
            flash('Recipe Edited.')
            return redirect(url_for('showRecipe', id=id))
    return render_template('editRecipe.html', recipe=recipe, name="Ecochef")


@application.route("/addToShoppingList/<ingredientIDs>")
def addToShoppingList(ingredientIDs):
    user = current_user
    
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
    
    return redirect(url_for('showShoppingList'))


@application.route("/removeFromShoppingList/<id>")
def removeFromShoppingList(id):
    return redirect(url_for('showShoppingList'))


@application.route("/shoppingList")
def showShoppingList():
    shoppingList = session['user'].shoppingList
    print(shoppingList)
    return render_template('shoppingList.html', user=current_user, shoppingList=shoppingList, name="Ecochef")


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    



  