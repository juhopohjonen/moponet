# Module for fetching and posting user related data.

from flask import Flask, jsonify, render_template, session, abort, \
    request, url_for, redirect

from user.user import user
from datahandling import dataHandler
import models
import app

import uuid
from sqlalchemy import desc, or_


def getMessageId(message):
    return message.id

# Get 'object' from (client side) session. Will return user_id.
# If it doesn't exist, then the wil return None -object. 

def get_uid_by_session(current_session):
    if 'object' in current_session:
        session = current_session['object']
        
        return session['user_id']
    else:
        return None


# API:s

@user.route('/followpoint', methods=['POST'])
def followpoint():
    # auth+json data required => throw error if not
    # authenticated or not data available

    Follow = models.Follow
    User = models.User

    db = app.db

    # does user want to SET follow status?
    # if not => default to GET status.
    isTypeSet = (request.args.get('type') == 'set')
    target_user_id = request.json['target_user_id']


    if 'object' not in session:
        abort(400)
    elif isTypeSet:
        # handle exception not mandatory data (target_user_id)
        try:
            isFollow = request.json['isFollow']
        except KeyError:
            abort(400)

    # fetch (follower) user

    follower_uid = get_uid_by_session(current_session=session)
    isOwner = (follower_uid == target_user_id)

    hasChangedStatus = False
    status = False

    # if user wants to SET following status
    if isTypeSet and not isOwner:
        hasChangedStatus = True

        # remove existing follow (follower and target user combo if exists)
        matching_follows = Follow.query.filter_by(
            follower=follower_uid,
            target_user=target_user_id
        ).all()

        for follow in matching_follows:
            db.session.delete(follow)

        # if user wants to follow: add follow.
        if isFollow:
            follow = Follow(
                follower=follower_uid,
                target_user=target_user_id
            )
            
            db.session.add(follow)
        
        db.session.commit()

    
    elif not isOwner:
       # = user wants to fetch follow data
       fetch_follow = Follow.query.filter_by(
            follower=follower_uid,
            target_user=target_user_id
       ).first()

       if fetch_follow != None:
        status=True


    response = {
        "isOwner": isOwner,
        "hasChangedStatus": hasChangedStatus,
        "hasUserFollowed": status
    }

    return jsonify(response)


def postDm(req):
    DirectMessage = models.DirectMessage
    User = models.User

    # validate data

    sender_id = get_uid_by_session(session)
    message = req.form.get('message')


    # validate data

    #if sender_id == None or req.form.get('recipient_id') == None \
    #    or message == None:
    #        abort(400)
    
    # make sure that the recipient id is valid
    try:
        recipient_id = int(req.form.get('recipient_id'))
        recipient = User.query.filter_by(id=recipient_id).first()
        
        if not recipient:
            raise
    except:
        abort(400)
    # Generate uuid for the message
    message_uuid = uuid.uuid4()

    message = DirectMessage(
        unique_str=str(message_uuid),
        sender_id=sender_id,
        recipient_id=recipient.id,
        message=message
    )

    # Add to the db + commit & return
    # the user to the chatView

    app.db.session.add(message)
    app.db.session.commit()

    return redirect(url_for('user.chatView', username=recipient.username) + "#" + message.unique_str)

@user.route('/directmessage/<string:username>')
def chatView(username):
    User = models.User
    DirectMessage = models.DirectMessage

    current_uid = get_uid_by_session(session)

    # require authentication
    if not current_uid:
        abort(401)

    chat_partner = User.query.filter_by(username=username).first_or_404()
    
    sent_messages = DirectMessage.query.filter_by(sender_id=current_uid).all()
    received_messages = DirectMessage.query.filter_by(recipient_id=current_uid).all()
    
    messages = []

    for message in sent_messages:
        messages.append(message)

    for message in received_messages:
        messages.append(message)

    messages.sort(key=getMessageId)

    return render_template(
        'chathistory.html',
        messages=messages,
        title=f'Keskusteluhistoria käyttäjän {chat_partner.username} kanssa',
        my_id=current_uid,
        chat_partner=chat_partner
    )