from config import Config
from models import *
from quicktype.recipeType import recipe_from_dict
from ingredient_parser import parse_ingredient
import datetime, chardet, json, os, requests

def allowed_file(filename):     
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def logThis(function, user, userID, recipe, recipeID):
    date = datetime.now()
    dateString = str(date)
    tuple = ('[',dateString,'] ',user,':',userID,' ',function,' ',recipe,':',recipeID)
    log = "".join(map(str, tuple))
    with open("log.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        file_object.write(log)
        
def get_token(user):
    url = Config.API_URL + "/login"

    payload = {}
    headers = {
    'Authorization': 'Basic dGVzdDp0ZXN0'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['token']
        
def populate():
    with open('allrecipes.json', 'rb') as f:
        result = chardet.detect(f.read())

    with open('allrecipes.json', encoding=result['encoding']) as f:
        data = json.load(f)
    
    for count, i in enumerate(data):
        recipe = recipe_from_dict(i)
        id = count
        title = recipe.title
        description = recipe.description
        category = recipe.category
        ratingAvg = recipe.aggregate_rating.rating_value
        ratingCount = recipe.aggregate_rating.rating_count
        prepTime = recipe.prep_time
        cookTime = recipe.cook_time
        servings = recipe.servings
        dateCreated = recipe.date_published
        
        instructions = []
        for step in recipe.instructions:
            instructions.append(step.text)
        
        # Get Image Url
        if recipe.image and recipe.image is not None:
            imageURL = recipe.image.url
        else:
            imageURL = 'default.jpg'
            
        
        # Get Video Url
        try:
            if recipe.video and recipe.video != 'No Video':
                videoURL = recipe.video.embed_url
        except:
            videoURL = 'No Video'
            
        
        new_recipe = Recipes(title=title,
                            category=category[0],
                            description=description,
                            instructions=instructions[0],
                            imageURL=imageURL,
                            videoURL=videoURL,
                            prepTime=prepTime,
                            cookTime=cookTime,
                            ratingAvg=ratingAvg,
                            ratingCount=ratingCount,
                            servings=servings,
                            dateCreated=dateCreated)
            
        for ingredient in recipe.ingredients:
            parsedIngredient = parse_ingredient(ingredient)
            print(parsedIngredient)
            newIngredient = Ingredients(name=parsedIngredient['name'], 
                                        amount=parsedIngredient['quantity'], 
                                        unit=parsedIngredient['unit'])
            new_recipe.ingredients.append(newIngredient)
       
            
        for review in recipe.reviews:
            review = Reviews(author=review.name, 
                             rating=review.rating, 
                             body=review.body)
            new_recipe.reviews.append(review)
        
        
        nutrition = Nutrition(calories = recipe.nutrition.calories,
                  carbohydrate = recipe.nutrition.carbohydrate,
                  cholesterol = recipe.nutrition.cholesterol,
                  fiber = recipe.nutrition.fiber,
                  protein = recipe.nutrition.protein,
                  saturatedFat = recipe.nutrition.saturated_fat,
                  sodium = recipe.nutrition.sodium,
                  sugar = recipe.nutrition.sugar,
                  fat = recipe.nutrition.fat,
                  unsaturatedFat = recipe.nutrition.unsaturated_fat) 
        new_recipe.nutrition.append(nutrition)
        
        print('NEW RECIPE =', new_recipe)
        db.session.add(new_recipe)
        db.session.commit()
    f.close()
    
def reverse_readline(filename, buf_size=8192):
    # A generator that returns the lines of a file in reverse order
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # The first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # If the previous chunk starts right from the beginning of line
                # do not concat the segment to the last line of new chunk.
                # Instead, yield the segment first 
                if buffer[-1] != '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment
