import pymongo
import sys
import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, abort, url_for, make_response



app = Flask(__name__)

#* Connected to MongoDB Database.
try:
  client = pymongo.MongoClient()
  
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)
@app.route('/')
def login():
    return render_template('login.html')