from flask import Blueprint, Flask, render_template
from datahandling import dataHandler
user = Blueprint('user', __name__, template_folder='templates', url_prefix='/user')

class userDataHandler(dataHandler):
    def __init__(self):
        # initialize object => import user class

        from models import User
        from flask import render_template

        self.model = User
        self.renderFunc = render_template


    # get user (query, find username) and return 
    # template rendering the user data
    def getUser(self, username):
        user = self.model.query.filter_by(username=username).first_or_404()
        return render_template('view_user.html',
        user=user,
        title=f'Käyttäjä {user.username}'
        )


    


@user.route('/<string:username>')
def view(username):
    handler = userDataHandler()
    
    return handler.getUser(username)