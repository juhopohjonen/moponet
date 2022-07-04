from flask_sqlalchemy import SQLAlchemy
from app import db

import json
from markupsafe import escape

import models


class User(db.Model):
    # Basic user columns (data to be stored in db)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(80), unique=True)

    # password can be true because users can authenticate
    # with external API.
    password = db.Column(db.String(1000), nullable=True)

    # isDiscordUser: if 1: true, if 0: false
    isDiscordUser = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User account (username: {self.username})'


# Class for comments about moped's
class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    # Comment's basic properties
    related_moped = db.Column(db.Integer(), nullable=False)
    commenter_username = db.Column(db.String(30), nullable=False)

    content = db.Column(db.Text(), nullable=False)

    def __repr__ (self):
        return f'<Comment, id={self.id}>'


# Like object for liking moped's
class Like(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    related_moped = db.Column(db.Integer(), nullable=False)
    liker_username = db.Column(db.String(30), nullable=False)


    # function for representing like
    def __repr__(self):
        return f'<Like id={self.id},\
            related_moped={self.related_moped}, \
                liker_username={self.liker_username}>'

class Follow(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    target_user = db.Column(db.Integer, nullable=False)
    follower = db.Column(db.Integer, nullable=False)

class Moped(db.Model):
    # Id's and owner info about the moped

    id = db.Column(db.Integer, primary_key=True)
    owner_username = db.Column(db.String(30), nullable=False)

    # Vehicle specific properties

    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    model_year = db.Column(db.Integer, nullable=False)

    # Store images path's and likes as STRING JSON at database column
    image_list = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Function for converting list of images to JSON (for storing in db as string)
    def list2json(list_of_images):
        return json.dumps(list_of_images)
        
    
    # Convert image_list column from json str to obj
    def json2list(self):
        return json.loads(self.image_list)

    
    # Get moped related data (likes and comments)
    # from database and return as object
    def get_related_data(self):
        likes = Like.query.filter_by(
            related_moped=self.id
        ).all()

        comments = Comment.query.filter_by(
            related_moped=self.id
        ).all()

        return {
            "likes": likes,
            "comments": comments
        }


    def __repr__ (self):
        return f'<Moped, id=({self.id}), owner_username=({self.owner_username})'

# DiscordUser for authenticating 
# related users
class DiscordUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # discord's own user identification property
    discord_uid = db.Column(db.String(250), nullable=False)

    # username of the user which is related to this
    # DiscordUser -object.
    related_username = db.Column(db.String(30), nullable=False)

    def __repr__():
        return f'<DiscordUser Object>'

class DirectMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_str = db.Column(db.String(100), nullable=False)

    sender_id = db.Column(db.Integer, nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)

    message = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Direct message from {self.sender_id} to {self.recipient_id}>'

class MopedMeet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, nullable=False)

    meet_name = db.Column(db.String(80), nullable=False)
    meet_description = db.Column(db.Text, nullable=False)
    meet_date = db.Column(db.DateTime, nullable=False)

    latitudes = db.Column(db.String(250), nullable=False)
    longitudes = db.Column(db.String(250), nullable=False)

    # convert all columns to dict
    def toDict(self):
        date = self.meet_date

        dict = {
            'id': self.id,
            'meet_name': escape(self.meet_name),
            'meet_description': escape(self.meet_description),

            'meet_day': date.strftime("%d"),
            'meet_month': date.strftime("%m"),
            'meet_year': date.strftime('%Y'),


            'latitudes': escape(self.latitudes),
            'longitudes': escape(self.longitudes)
        }

        return dict

    def getParticipants(self):
        User = models.User
        raw = MeetParticipant.query.filter_by(meet_id=self.id).all()
        
        participants = []
        for raw_participant in raw:
            participants.append({
                'username': User.query.get(raw_participant.participant_id).username
            })

        return participants

    def __repr__(self):
        return f'<MopedMeet called "{self.meet_name}">'


class MeetParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    participant_id = db.Column(db.Integer, nullable=False)
    meet_id = db.Column(db.Integer, nullable=False)