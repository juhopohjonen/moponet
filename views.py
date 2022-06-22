# This module contains URL routing map functions and urls.

from flask import Flask, jsonify, render_template, request

from app import app
from datahandling import *

from harpatykset import *
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
            title='Rekisteröidy',
            paskaMopo=getPaskaMopo()
        )
    elif request.method == 'POST':
        return process_registration_request(raw_data=request.data)

@app.route('/login', methods=["GET", "POST"])
def login():
    # Does user want to GET login_page or POST login data?
    if request.method == 'GET':
        return render_template(
            'forms/log/login_page.html',
            title='Kirjaudu sisään',
            
            # Some swear words to
            # help with 'vitutus' when
            # you can't remember your pass.

            swear_word=swear()
        )
    elif request.method == "POST":
        return process_login_user(
            request_form=request.form,
            error_page='errors/user_not_found.html'
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


# return user public images when
# called imagepoint
@app.route('/imagepoint/<name>')
def imagepoint(name):
    return download_file(name, app.config["UPLOAD_FOLDER"])

@app.route('/licences')
def licences():
    return """Copyright (c) 2022 by Doan Ngoc Thuong (https://codepen.io/ngthuongdoan/pen/wvWvbbj)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""