import pymongo
import sys
import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app = Flask(__name__)

#* Connected to MongoDB Database.

try:
  client = pymongo.MongoClient("mongodb+srv://jaar2023:me8rd2iS73YJLTfW@recipes01.ajqwb7q.mongodb.net/?retryWrites=true&w=majority")
  
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

# create the user and recipes collection
users = client.RecipeApp
# TODO: Everyone add in your name in the database (through the web)

# login screen 
@app.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # read user collection for existing account 
    user = db.user_collection.find_one({
    "username": username,
    "password": password
})
    
    if user and password:
        return redirect(url_for('mainscreen'))
    else:
        return redirect(url_for('createprofile'))

# create profile form
@app.route('/createprofile', methods=['POST'])
def createprofile():
        name = request. form['name']
        username = request.form['username']
        password = request.form['password']


        profile = {
            "name": name,
            "username": username,
            "password": password
        }

        user_collection.insert_one(profile)
        return redirect(url_for('mainscreen'))

# view main recipe screen
@app.route('/mainscreen')
def view_mainscreen():
    return render_template('mainscreen.html')

# view add recipe screen
@app.route('/addscreen')
def show_addscreeb():
    return render_template('addscreen.html')

# view edit recipe screen
@app.route('/editscreen')
def show_editscreen():
    return render_template('editscreen.html')

# view delete recipe screen
@app.route('/deletescreen')
def show_deletescreen():
    return render_template('deletescreen.html')

# view recipe screen
@app.route('/recipescreen')
def show_recipescreen():
    return render_template('viewscreen.html')

# view create profile screen
@app.route('/createprofile')
def show_createprofile():
    return render_template('createprofile.html')



