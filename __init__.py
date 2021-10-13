from flask import Flask
import json
import pymongo


app=Flask(__name__)
app.secret_key='secretkey'
app.config['MONGO_URI'] = 'mongodb://localhost:27017'

