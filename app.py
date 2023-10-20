import sys
import os
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

#* Connected to MongoDB Database.

try:
  client = pymongo.MongoClient(token)
  
# return a friendly error if a URI error is thrown 
# Todo: Fix issue with logging error including the port.
#? For some reason when I do flask --app app run it logs the port message into the error log.
except pymongo.errors.ConfigurationError as e:
  logging.error("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

# create the user and recipes collection
db = client.RecipeApp
users = db.get_collection('Users')

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
    # get values from HTML form found in login.html
    username = request.form.get('username')
    password = request.form.get('password')

    # read user collection for existing account 
    profile = users.find_one({
    "username": username,
    "password": password
    })

    if profile:
        session['username'] = username  #saving username in session so it can be used in other functions == not localized
        return redirect(url_for('mainscreen'))
    else:
        return redirect(url_for('createprofile'))
    
# create profile form
@app.route('/createprofile', methods=['POST'])
def createprofile():
        # get values from HTML form found in createprofile.html
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        #todo: Verification! @Jhon
        user_exists = users.find_one({"username": username})

        if user_exists:
            return "User already exists" #should create like pop up in front end to let user know
        else:
            profile = {
                "name": name,
                "username": username,
                "password": password
            }
            users.insert_one(profile)

        #Todo: Add user to database
        
        #TODO: 
        return redirect(url_for('mainscreen'))

# view main recipe screen
@app.route('/mainscreen')
def view_mainscreen(): 
    username = session.get('username')
    user_data = users.find_one({"username": username})
    if user_data and 'recipes' in user_data:
        return render_template('mainscreen.html', recipes=user_data['recipes'])
    return render_template('mainscreen.html')

# view add recipe screen
@app.route('/addscreen', methods=['GET', 'POST'])
def show_addscreen():
    username = session.get('username')
    if request.method == 'GET': #this is by default to show form to user
        return render_template('addscreen.html')
    elif request.method == 'POST': #this is to save users input plz make sure there the save button is with POST request
        recipe_name = request.form['recipe_name']
        cook_time = request.form['cook_time']
        ingredients = request.form['ingredients'] #any format, should we specify? => REACH goal
        instructions = request.form['instructions'] #parsing => REACH goal

        #creating the JSON(?) object for the new recipe
        new_recipe = {
            "name": recipe_name,
            "cook_time": cook_time,
            "ingredients": ingredients,
            "instructions": instructions
        }
        #assuming the user is already logged in & you have their username available
        users.update_one({"username": username}, {"$push": {"recipes": new_recipe}}) #$push is MongoDB operator that appens this value into recipes array
        return redirect(url_for('mainscreen'))

# view edit recipe screen
@app.route('/editscreen/<recipe_name>', methods=['GET', 'POST']) #need to add "Edit" button with a link to /editscreen/<recipe_name> per recipe !frontend thing!
def show_editscreen(recipe_name):
    if request.method == 'GET': #default screen to show edit recipe screen
        return render_template('editscreen.html', recipe_name=recipe_name)
    elif request.method == 'POST': #user's decision to save or not



@app.route('/editscreen/<recipe_name>', methods=['GET', 'POST'])
def show_editscreen(recipe_name):
    username = session.get('username')
    user_data = users.find_one({"username": username})
    
    current_recipe = None
    for recipe in user_data['recipes']:
        if recipe['name'] == recipe_name:
            current_recipe = recipe
            break

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
            username = session.get('username')
            users.update_one({"username": username}, {"$pull": {"recipes": {"name": recipe_name}}}) # delete using the name
        return redirect(url_for('mainscreen')) #going back to mainscreen

#viewing specific recipe
@app.route('/recipescreen/<recipe_name>')
def show_recipescreen(recipe_name):
    username = session.get('username')
    user_data = users.find_one({"username": username})
    return render_template('viewscreen.html')

# view profile that is already created
@app.route('/createprofile', methods=['GET'])
def show_createprofile():
    return render_template('createprofile.html')