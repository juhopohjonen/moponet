from flask import Blueprint, Flask, render_template
from datahandling import dataHandler
import json
import models

import user.userhandling as userhandling

import restrictViews as restrict
user = Blueprint('user', __name__, template_folder='templates', url_prefix='/user',
static_folder='userstatic')



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


    # get user (query, find username) and return
    # the user object (=None if user does not exist)
    def getUser_norender(self, username):
        user = self.model.query.filter_by(username=username)
        return user
    


@user.route('/<string:username>', methods=['GET', "POST"])
def view(username):

    # only accept POST if user
    # wans to post a message, then 

    if request.form.get('type') == 'directmessage' \
        and request.method == 'POST' and \
            userhandling.get_uid_by_session(session) != None:
                return userhandling.postDm(req=request)
    elif request.method == 'POST':
        abort(405)

    # view info about the profile
    user = models.User.query.filter_by(username=username).first_or_404()

    # render 30 moped objects server side and
    # more asyncronoysly (via xmlhttprequest)
    # with JavaScript.

    raw_moped_objects = models.Moped.query.filter_by(
        owner_username=username
    ).order_by(
        models.Moped.id.desc()
        ).limit(30).all(
    )

    moped_list = []
    for moped in raw_moped_objects:
        related_data = moped.get_related_data()
        moped_content = {
            'object': moped,
            'moped_images': json.loads(moped.image_list),
            'default_image': json.loads(moped.image_list)[0],
            'likes': related_data['likes'],
            'comments': related_data['comments']
        }

        moped_list.append(moped_content)
        
    return render_template(
        'view_user.html',
        title=f"Käyttäjä '{user.username}'", 
        user=user,
        mopeds=moped_list
    )


@user.route('/me')
def my_profile():
    # redirect user to the user profile

    User = models.User

    uid = userhandling.get_uid_by_session(session)

    if uid == None:
        return redirect(url_for('home')), 401

    current = User.query.get(uid)

    return redirect(url_for('user.view', username=current.username))

# view direct messages
@user.route('/directmessage')
@user.route('/directmessage/')
def senderList():

    userid = userhandling.get_uid_by_session(session)
    if not userid:
        abort(401)

    DirectMessage = models.DirectMessage
    User = models.User

    sentMessages = DirectMessage.query.filter_by(sender_id=userid).all()
    receivedMessages = DirectMessage.query.filter_by(recipient_id=userid).all()

    userids = []
    print (userids)


    for message in sentMessages:
        id = message.recipient_id
        if id not in userids:
            userids.append(id)

    for message in receivedMessages:
        id = message.sender_id
        if id not in userids:
            userids.append(id)

    # fetch usernames
    senders = []
    for uid in userids:
        Username = User.query.filter_by(id=uid).first()
        senders.append(Username)

    return render_template(
        'directmsg.html',
        title='Yksityisviestit',
        senders=senders
    )

# Import user authentication module
from user.userauth import *