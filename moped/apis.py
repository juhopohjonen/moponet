from flask import Flask, redirect, request, jsonify, Blueprint, session, abort, url_for
import app
import moped.moped as m_source
import models

import user.userhandling as userhandling

moped = m_source.moped

# aplication programming interfaces


# API for commenting about mopeds.
@moped.route('/api/comment', methods=['POST'])
def comment():
    # get form & comment objects
    form = request.form
    comment = form.get('comment')

    userId = userhandling.get_user_session(session)
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
    
