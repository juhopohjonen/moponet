from crypt import methods
from flask import Flask, redirect, request, jsonify, Blueprint, session, abort, url_for
import app
import moped.moped as m_source
import models
import json

import user.userhandling as userhandling
import user.user as user

moped = m_source.moped

# aplication programming interfaces


# API for commenting about mopeds.
@moped.route('/api/comment', methods=['POST'])
def comment():
    # get form & comment objects
    form = request.form
    comment = form.get('comment')

    userId = userhandling.get_uid_by_session(session)
    mopedId = form.get('moped_id')

    # if userId returns none or no comment data at comment, 
    # then abort => 400.
    if userId == None \
        or comment == None \
            or comment == '':
                abort(400)

    
    # abort 400 if no moped id or no object
    # in database

    Moped = models.Moped

    if mopedId == None \
        or Moped.query.filter_by(id=mopedId) \
            .first() == None:
                abort(400)

 
    # fetch user based on userId
    User = models.User
    current_user = User.query.filter_by(id=userId).first_or_404()


    # Import & Create instance of comment 
    Comment = models.Comment
    current_comment = Comment(
        related_moped=mopedId,
        commenter_username=current_user.username,
        content=comment
    )

    db = app.db

    # Add comment (obj) to db (via sqlalchemy)
    # and commit changes.

    db.session.add(current_comment)
    db.session.commit()

    # redirect user to the comment view.

    return redirect(
        url_for('moped.view', id=mopedId) + '#comment-' + str(current_comment.id)
    )
    

# API for fetching has user liked

@moped.route('/api/like_status/<int:mopedid>', methods=['POST'])
def like_status_api(mopedid):

    # require authentication, if not authenticated
    # then return 401
    user_id = userhandling.get_uid_by_session(
        current_session=session
    )

    if user_id == None:
        abort(401)

    # import base classes
    Moped = models.Moped
    Like = models.Like
    User = models.User
    
    # get mopedid from the dynamic parameter
    # => fetch moped obj based on the id
    
    related_moped = Moped.query.filter_by(
        id=mopedid
    ).first_or_404()
    
    
    # init userhandler & get user obj
    # based on user_id

    username = User.query.filter_by(
        id=user_id
    ).first().username


    # fetch likes results
    like = Like.query.filter_by(
        liker_username=username,
        related_moped=mopedid
    ).first()


    # Has user liked? return result as json.
    hasUserLiked = (like != None)

    return jsonify({
        "hasUserLiked": hasUserLiked
    })


@moped.route('/api/like/<int:mopedid>', methods=['POST'])
def changeLike(mopedid):
    # in likeType param: 1 = true, 0 = false
    likeType = request.args.get('like')

    # require authentication, if not authenticated
    # then return 401
    user_id = userhandling.get_uid_by_session(
        current_session=session
    )

    if user_id == None:
        abort(401)


    # IF mandatory information (like or 
    # dislike) is not
    # valid: return client side error 400

    if likeType != '0' and likeType != '1':
        abort(400)

    # convert liketype to boolean
    doesUserWantToLike = (likeType == '1')

    # import base classes
    Moped = models.Moped
    Like = models.Like
    User = models.User
    
    # get mopedid from the dynamic parameter
    # => fetch moped obj based on the id
    
    related_moped = Moped.query.filter_by(
        id=mopedid
    ).first_or_404()
    
    
    # init userhandler & get user obj
    # based on user_id

    username = User.query.filter_by(
        id=user_id
    ).first().username


    # fetch likes results
    likes = Like.query.filter_by(
        liker_username=username,
        related_moped=mopedid
    ).all()

    # import db
    db = app.db

    # remove all matching likes from db and commit (if exists)
    for like in likes:
        db.session.delete(like)

    # if user wants to like
    # then create new like object.
    if doesUserWantToLike:
        current_like = Like(
            related_moped=mopedid,
            liker_username=username
        )

        db.session.add(current_like)

    # commit changes.
    db.session.commit()

    return jsonify({
        "message": "success"
    })

# function for fetching mopeds via ajax,
# no need for refreshing 
@moped.route('/api/fetchmopeds', methods=['GET', 'POST'])
def fetch_mopeds_api():

    Moped = models.Moped

    mandatory_args = [
        'start'
    ]

    for arg in mandatory_args:
        if request.args.get(arg) == None:
            abort(400)

    start_arg = request.args.get('start')
    
    # try to convert arg (string)
    # to int, if cannot: then not valid
    # argument => return 400

    try:
        start = int(start_arg)
    except:
        abort(400)

    allmopeds = Moped.query.all()

    # return no_mopeds as status if
    # there is not more mopeds to load 
    if start > len(allmopeds):
        return jsonify({
            "status": "no_mopeds"
        })

    # return mopeds as moped_content dir
    # which contains also related data
    # eg. photos, likes, comments
    moped_list = []

    lastMopedID = 0

    for moped in allmopeds:

        if len(moped_list) > app.configuration['RENDERED_MOPED_OBJECTS'] - 1:
            # return only 20 mopeds at one time (limit
            # with break)
            break
        
        related_data = moped.get_related_data()
        moped_content = {
            'object': {
                "id": moped.id,
                "owner_username": moped.owner_username,
                "brand": moped.brand,
                "model": moped.model,
                "model_year": moped.model_year
            },
            'moped_images': json.loads(moped.image_list),
            'default_image_url': url_for('moped.mopedimages', name=json.loads(moped.image_list)[0]),
            'likes_len': len(related_data['likes']),
            'comments_len': len(related_data['comments'])
        }

        lastMopedID = moped.id

        if allmopeds.index(moped) > start - 2:
            moped_list.append(moped_content)


    # return: Is there more moped objects?
    isThereMore = (lastMopedID < len(allmopeds))
    
    return jsonify({
        "status": "success",
        "mopeds": moped_list,
        "isThereMore": isThereMore,
    })