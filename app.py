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
@app.route('/',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # read user collection for existing account 
    user = db.user_collection.find_one({
    "username": username,
    "password": password
})
    
    if user and password:
        return redirect(url_for('main'))
    else:
        return redirect(url_for('createprofile'))


# main recipe screen
@app.route('/mainscreen')
def main():
    return render_template('mainscreen.html')

# add recipe screen
@app.route('/addscreen')
def main():
    return render_template('addscreen.html')

# edit recipe screen
@app.route('/editscreen')
def main():
    return render_template('editscreen.html')

# delete recipe screen
@app.route('/deletescreen')
def main():
    return render_template('deletescreen.html')

# view recipe screen
@app.route('/viewscreen')
def main():
    return render_template('viewscreen.html')

# create profile screen
@app.route('/createprofile')
def main():
    return render_template('createprofile.html')

