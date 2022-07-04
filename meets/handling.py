from flask import Flask, jsonify, redirect, render_template, request, abort, url_for, session
from meets.meets import meets
import json

import models
import user.userhandling as userhandling

from app import db

from datetime import datetime as timelib

@meets.route('/fetchmeets', methods=['POST'])
def fetchmeets():
    # fetch all meets from db
    Meet = models.MopedMeet
    meetObjects = Meet.query.all()

    
    meets = []
    for meet in meetObjects:
        meets.append(meet.toDict())

    msg = {
        'meets': meets
    }

    return jsonify(msg)


# url for showing user info about the meet
@meets.route('/viewmeet/<int:id>')
def viewmeet(id):
    Meet = models.MopedMeet
    User = models.User
    
    meet = Meet.query.filter_by(id=id).first_or_404()

    # fetch info about the organizer too
    organizer = User.query.get(meet.organizer_id)

    return render_template(
        'viewmeet.html',
        title=f"Mopomiitti '{meet.meet_name}'",
        meet=meet,
        meetDict=meet.toDict(),
        organizer=organizer,
        participants=meet.getParticipants()
    )


# Function for creating a meet
@meets.route('/create', methods=['POST'])
def create_meet():
    # try to convert data to json + check mandatory vars
    # if cannot or not vars: throw error with status 400

    mandatory_vars = ['name', 'description', 'lat', 'lon', 'date']

    try:
        data = json.loads(request.data)

        for var in mandatory_vars:
            if var not in data:
                raise


        # try to parse the meet date
        date = timelib.strptime(data['date'], '%Y-%m-%d')


        # also check sign in status
        userid = userhandling.get_uid_by_session(session)

        if userid == None:
            raise
    except:
        abort(400)

    print(f'date value: {str(date)}, type: {type(date)}')

    name = data['name']
    description = data['description']
    lat = data['lat']
    lon = data['lon']

    # create new Meet object based on users input
    # and add into the session + commit

    Meet = models.MopedMeet
    current = Meet(
        organizer_id=userid,
        meet_name=name,
        meet_description=description,
        latitudes=lat,
        longitudes=lon,
        meet_date=date
    )

    db.session.add(current)
    db.session.commit()
    
    msg = {
        'isRedirect': True,
        'redirecturl': url_for('meets.viewmeet', id=current.id)
    }

    return jsonify(msg)


@meets.route('/participate', methods=['POST'])
def participate():

    Participant = models.MeetParticipant
    Meet = models.MopedMeet

    # fetch user profile (if not signed in or no meet id => error)
    userid = userhandling.get_uid_by_session(session)
    str_meetid = request.args.get('meetid')

    if userid == None:
        abort(401)
    

    try:
        # try to change meetid arg to int (defaults: str)
        if str_meetid == None:
            raise

        meetid = int(str_meetid) 
        
        # validate that meet exists
        current_meet = Meet.query.filter_by(id=meetid).first()
        
        if current_meet == None:
            raise



    except Exception as e:
        print(e)
        abort(400)

    # return status of participation (t/f) if user requests it

    if request.args.get('type') == 'getparticipation':
        
        result = Participant.query.filter_by(
            participant_id=userid,
            meet_id=meetid
        ).first()

        hasParticipated = (result != None)

        return jsonify({
            'hasParticipated': hasParticipated
        })

    # remove all current meet related
    # participation objs from db
    # and create new participation obj

    participationObjs = Participant.query.filter_by(
        participant_id=userid,
        meet_id=meetid
    ).all()

    # remove all existing participations

    for obj in participationObjs:
        db.session.delete(obj)

    # try to parse request data: does user want to
    # participate or cancel the participation?

    try:
        data = json.loads(request.data)
        wantsToParticipate = data['wantsToParticipate']
    except:
        abort(400)


    # add new participant to the session
    # IF the user wants to participate.


    if wantsToParticipate:

        new = Participant(
            participant_id=userid,
            meet_id=meetid,
        )
        
        db.session.add(new)

    db.session.commit()

    return jsonify({
        'msg': 'success'
    })