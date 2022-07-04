# This module contains URL routing map functions and urls.

from flask import Flask, jsonify, render_template, request

from app import app
from datahandling import *

from datetime import date, datetime

from restrictViews import render_restricted

@app.route('/')
def home():
    return render_template(
        'index.html',
        title='Etusivu'
    )


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Does user want to GET signup_page or POST signup data?
    if request.method == 'GET':
        return render_template(
            'forms/log/signup_page.html',
            title='Rekisteröidy'
        )
    elif request.method == 'POST':
        return process_registration_request(raw_data=request.data)

@app.route('/login', methods=["GET", "POST"])
def login():
    # Does user want to GET login_page or POST login data?
    if request.method == 'GET':
        return render_template(
            'forms/log/login_page.html',
            title='Kirjaudu sisään'
        )
    elif request.method == "POST":
        return process_login_user(
            request_form=request.form,
            error_page='errors/user_not_found.html',
            r=request
        )



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Does user want to GET logout_page or POST logout request?
    if request.method == 'GET':
        return render_template(

            'forms/log/logout_page.html',
            title='Kirjaudu ulos'
        )
    else:
        process_user_logout(session=session)
        
        return render_template(
            'forms/log/logout_page.html',
            title='Olet uloskirjautunut'
        )



