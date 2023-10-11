import pymongo
import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app = Flask(__name__)

# make a connection to the database server
connection = pymongo.MongoClient("your_db_host", 27017,
                                username="your_db_username",
                                password="your_db_password",
                                authSource="your_db_name")

# select a specific database on the server
db = connection["your_db_name"]

# create the user and recipes collection
user_collection = db["users"]
recipes_collection = db["recipes"]

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


