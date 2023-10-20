import sys
import os
import User
import logging
from flask import Flask, render_template, request, redirect, abort, url_for, make_response, session
import pymongo
from dotenv import load_dotenv 
import datetime
from bson.objectid import ObjectId
from pymongo.errors import ConfigurationError

app = Flask(__name__)
load_dotenv()
token = os.getenv('DB_CONNECTION_STRING')
# # * Set-up error logger.
logging.basicConfig(filename='error.log', level=logging.ERROR)
logging.basicConfig(filename='debug.log', level=logging.INFO)
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
#* Connected to MongoDB Database.
if __name__ == "__main__":
    app.run(debug=True)
try:
  client = pymongo.MongoClient(token)
  logger.info("Successfully connected to db.")

# return a friendly error if a URI error is thrown 
# Todo: Fix issue with logger error including the port.
#? For some reason when I do flask --app app run it logs the port message into the error log.
except pymongo.errors.ConfigurationError as e:
  logger.error("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

# create the user and recipes collection
db = client.RecipeApp
users = db.get_collection('Users')
currUser = None
#Current user mapper
def map_json_to_user(json_obj):
    try:
        name = json_obj.get("name")
        username = json_obj.get("username")
        age = json_obj.get("age")
        recipes = json_obj.get("recipes", {})
        u = User(name, username, age, recipes)
        logger.info(f"{u} was created")
        return u
    except Exception as e:
        logger.error("MAPPING ERROR: error in mapping JSON to user.")
def map_user_to_json(user):
    try:
        user_data = {
            "name": user.name,
            "username": user.username,
            "age" : user.age,
            "recipes": user.recipes
        }
        return user_data
    except Exception as e:
        logger.error("MAPPING ERROR: error in mapping user to JSON.")
@app.route('/')
def view_dashboard():
    return render_template('index.html')

# Generate login page
@app.route('/loginpage', methods=['GET'])
def generate_login_page():
    return render_template('login.html')
# login screen 
@app.route('/login',methods=['POST'])
def login():
    global currUser
    # get values from HTML form found in login.html
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        logger.info("Information from front-end retrieved successfully.")
    except Exception as e:
        logger.error("RETRIEVAL ERROR: Problem retrieving info from front-end.")

    # read user collection for existing account 
    
    profile = users.find_one({
    "username": username,
    "password": password
    })
    
    if profile:
        currUser = map_json_to_user(profile)  #saving username in session so it can be used in other functions == not localized
        logger.info(f"User has been logged in with username: ({currUser.username}) .")
        return redirect(url_for('mainscreen'))
    else:
        #Todo: Change to printing "incorrect username or password"
        return redirect(url_for('createprofile'))
    
# create profile form
@app.route('/createprofile', methods=['POST'])
def createprofile():
        global currUser
        # get values from HTML form found in createprofile.html
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        #* Verification! @Jhon
        user_exists = users.find_one({"username": username})

        if user_exists:
            #Todo: @Alex and @Aaron
            return "User already exists" #should create like pop up in front end to let user know
        else:
            try:
                currUser = User(name, username, password)
                jsonUser = map_user_to_json(currUser)
                logger.info(f"Successfully created JSON User to be inserted in database with username {jsonUser.get(username)} .")
                users.insert_one(jsonUser)
                return redirect(url_for('mainscreen'))
            except Exception as e:
                logger.error(f"AMBIGUOUS ERROR:Unsuccessfull profile creation. Error code: {e}")
        

# view main recipe screen
@app.route('/mainscreen')
def view_mainscreen():
    global currUser
    #If none then redirect to mainpage
    if currUser is None:
        return render_template("index.html")
    #else continue
    #todo: Stress test for 0 recipes and for 1 recipe
    if len(currUser.recipes) > 0:
        return render_template('mainscreen.html', recipes=currUser.recipes)
    return render_template('mainscreen.html')

# view add recipe screen
@app.route('/addscreen', methods=['GET', 'POST'])
def show_addscreen():
    global currUser
    if request.method == 'GET': #this is by default to show form to user
        return render_template('addscreen.html')
    elif request.method == 'POST': #this is to save users input plz make sure there the save button is with POST request
        
        #* Retrieve add information.
        recipe_name = request.form['recipe_name']
        cook_time = request.form['cook_time']
        ingredients = request.form['ingredients'] #any format, should wef specify? => REACH goal
        instructions = request.form['instructions'] #parsing => REACH goal
        currUser.recipes.ingredients()
        #creating the JSON(?) object for the new recipe
        new_recipe = {
            "name": recipe_name,
            "cook_time": cook_time,
            "ingredients": ingredients,
            "instructions": instructions
        }
        #assuming the user is already logged in & you have their username available
        users.update_one({"username": currUser.username}, {"$push": {"recipes": new_recipe}}) #$push is MongoDB operator that appens this value into recipes array
        logger.info("No error so far in recipe addition")
        return redirect(url_for('mainscreen'))
    
@app.route('/editscreen/<recipe_name>', methods=['GET', 'POST'])
def show_editscreen(recipe_name):
    username = session.get('username')
    user_data = users.find_one({"username": username})
    
    current_recipe = None
    for recipe in user_data['recipes']: #getting specific recipe
        if recipe['name'] == recipe_name:
            current_recipe = recipe
            break
    
    if request.method == 'GET': 
        return render_template('editscreen.html', recipe=current_recipe)
    
    elif request.method == 'POST': #if user's clicks on save button
        updated_name = request.form['recipe_name']
        updated_cook_time = request.form['cook_time']
        updated_ingredients = request.form['ingredients']
        updated_instructions = request.form['instructions']

        #updating
        current_recipe['name'] = updated_name
        current_recipe['cook_time'] = updated_cook_time
        current_recipe['ingredients'] = updated_ingredients
        current_recipe['instructions'] = updated_instructions

        #pushing updated recipe into the database
        users.update_one(
            {"username": username, "recipes.name": recipe_name},
            {"$set": {
                "recipes.$.name": updated_name,
                "recipes.$.cook_time": updated_cook_time,
                "recipes.$.ingredients": updated_ingredients,
                "recipes.$.instructions": updated_instructions
            }}
        )
        return redirect(url_for('mainscreen'))

# view delete recipe screen
@app.route('/deletescreen/<recipe_id>', methods=['GET', 'POST']) #need recipe_id for specific recipe deletion
def show_deletescreen(recipe_name): #need to pass recipe_id as an arugment
    if request.method == 'GET': #default screen to show delete recipe screen
        return render_template('deletescreen.html', recipe_name=recipe_name)
    elif request.method == 'POST': #user's decision to delete or not
        decision = request.form.get('decision')  #on front-end please name the yes or no buttons 'decision 
        if decision == 'yes':
            username = currUser.email
            users.update_one({"username": username}, {"$pull": {"recipes": {"name": recipe_name}}}) # delete using the name
        return redirect(url_for('mainscreen')) #going back to mainscreen

#viewing specific recipe
@app.route('/recipescreen/<recipe_name>')
def show_recipescreen(recipe_name):
    username = currUser.email
    user_data = users.find_one({"username": username})
    return render_template('viewscreen.html')

# view profile that is already created
@app.route('/createprofile', methods=['GET'])
def show_createprofile():
    return render_template('createprofile.html')