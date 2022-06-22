
from flask import Flask, jsonify, abort, redirect, render_template, url_for, session, send_from_directory
from app import app, db

import models

from werkzeug.security import generate_password_hash, check_password_hash


class dataHandler:
    def __init__(self, allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

import json

class sessionObject:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def generate_dict(self):
        return {
            "user_id": self.user_id
        }
    

def get_id_session_obj(object):
    return object['user_id']

def create_user (username, email, unhashed_pwd):
    # Create password hash and user object with it
    User = models.User
    
    password_hash = generate_password_hash(unhashed_pwd)
    
    current_user = User(username=username, email=email, password=password_hash)

    # Commit changes and return current_user.
    db.session.add(current_user)
    db.session.commit()

    return current_user

def process_registration_request(raw_data):
    User = models.User

    # Get data from form and make sure every value exist and value length is OK
    # If value doesn't exist, abort request => return error
    try:
        data = json.loads(raw_data)
        
        userdata = {
            "username": data["username"],
            "email": data["email"],
            "password": data["password"]
        }

        if userdata["username"] is None \
            or userdata ["email"] is None \
                or userdata ["password"] is None:
                raise
    except:
        abort(400)



    # Does user exist? If so, return an error.

    existing_email = User.query.filter_by(email=userdata["email"]).first()
    existing_username = User.query.filter_by(username=userdata["username"]).first()

    if existing_email is None and existing_username is None:
        existing_user = None
    else:
        existing_user = True

    if existing_user == True:
        return jsonify({
            "message": "Käyttäjänimi tai sähköposti on jo käytössä."
        }), 400

    # create user and log it, store current_session_object contents as dictionary (serializable to JSON)
    useraccount = create_user(userdata["username"], userdata["email"], userdata["password"])
    
    current_session_object = sessionObject(user_id=useraccount.id)
    session["object"] = current_session_object.generate_dict()

    # SUCCESS, return to homepage :D

    return jsonify({
        "message": "success",
        "redirect_url": url_for('home')
    })

def process_login_user(request_form, error_page):

    # get username+password form form data

    username = request_form.get('username')
    password = request_form.get('password')

    # confirm that username & password aren't null

    if username == None or \
        password == None:
        
        abort(400)

    # query the db for records

    current_user = models.User.query.filter_by(username=username).first()

    if current_user is None:
        # user not found, render not found site
        return render_template(error_page)


    # check password hash, if not valid, then password not correct. => return user not found
    if check_password_hash(current_user.password, password) == False:
        return render_template(error_page)

    

    # log in user, store current_session_object contents as dictionary (serializable to JSON)
    current_session_object = sessionObject(user_id=current_user.id)
    session["object"] = current_session_object.generate_dict()


    # Redirect to homepage
    return redirect(url_for('home'))

def process_user_logout (session):

    # Log user out (pop 'object' from session) if 
    # user is logged in. (object in session)

    if 'object' in session:
        session.pop('object')

def download_file(name, upload_folder):
    return send_from_directory(upload_folder, name)