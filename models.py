from flask_sqlalchemy import SQLAlchemy
from app import db

import json


class User(db.Model):
    # Basic user columns (data to be stored in db)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(1000))

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