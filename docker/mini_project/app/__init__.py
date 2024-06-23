from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://admin:password@mongodb:27017/mydatabase'
mongo = PyMongo(app)

