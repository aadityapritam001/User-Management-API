from flask import Flask, render_template , jsonify , request, Response, session, url_for,redirect
import bcrypt
import uuid
import json
from __init__ import app
from datetime import datetime
from pymongo import MongoClient
import jwt
from functools import wraps
import random

app = Flask(__name__)
app.secret_key = "abd"
client = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = client.get_database('user_details')
records = db['user']


@app.route('/',methods=['POST'])
def home():
    if "username" in session:
        return "{} Session is running !".format(session['username'])
    else:
        return "please login or register yourself first"

# def token_required(f):
#    @wraps(f)
#    def decorator(*args, **kwargs):
#        token = None
#        if 'x-access-tokens' in request.headers:
#            token = request.headers['x-access-tokens']
 
#        if not token:
#            return jsonify({'message': 'a valid token is missing'})
#        try:
#            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#            current_user = Users.query.filter_by(public_id=data['public_id']).first()
#        except:
#            return jsonify({'message': 'token is invalid'})
  
#        return f(current_user, *args, **kwargs)
#    return decorator

@app.route('/signup', methods=['POST'])
def index():
    message = ''
    # if "username" in session:
    #     return "Already logged In"
    if request.method == "POST":
        user_data=request.json
        user =  user_data["username"]
        email = user_data["email"]
        phone_no = user_data["phone_no"]
        password1 = user_data["password1"]
        password2 = user_data["password2"]
        user_found = records.find_one({"username": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return jsonify(message)
        if email_found:
            message = 'This email already exists in database'
            return jsonify(message)
        if password1 != password2:
            message = 'Passwords should match!'
            return jsonify(message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            uid=uuid.uuid4()
            user_input = {'merchant id':uid, 'username': user, 'email': email, 'phone no':phone_no,'password': hashed}
            records.insert_one(user_input)
            resp=jsonify({'merchant id':uid,'message':'{} Registered successfully ! '.format(user)})
            resp.status_code=201
            session['username']=user  
            # session.commit()
            return resp
    
    resp=jsonify({'Message':'request Methods Error'})
    resp.status_code=400
    return resp



@app.route("/login", methods=["POST", "GET"])
def login():
    message0 = 'Please login to your account'
    # if "user" in session:
    #     return "You are already logged In"

    if request.method == "POST":
        log_info= request.json
        user=log_info['username']
        password = log_info["password"]

       
        user_found = records.find_one({"username": user})
        Merchant_id=user_found['merchant id']
        if user_found:
            user_val = user_found['username']
            passwordcheck = user_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["username"] = user_val
                return "Logged In Successfully! merhcant_id :{}".format(Merchant_id)
            else:
                if "user" in session:
                    return "Already Logged In "
                message = 'Wrong password'
                return message
        else:
            message = 'Username not found'
            return message
    return message0


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "username" in session:
        session.pop("username", None)
        return "You are logged Out !"
    else:
        return "Please Login First!"


#end of code to run it
if __name__ == "__main__":
  app.run(debug=True)