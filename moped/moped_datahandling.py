# file for handling moped specific data.


from werkzeug.utils import secure_filename
from models import Moped, User
import os
from app import app
import user.user as userPackage

import json
from restrictViews import generateSomeRandomString


import datahandling

from flask_sqlalchemy import SQLAlchemy
from moped import moped
# mopedDataHandler class for handling moped data.
# Inherits from dataHandler.

from datahandling import dataHandler, get_id_session_obj
class mopedDataHandler(dataHandler):
    def __init__(self, current_session):

        # get packages, store into object.
        from flask import abort, request, redirect, url_for, render_template
        
        import app
        
        UPLOAD_EXTENSIONS = app.UPLOAD_EXTENSIONS

        self.abort = abort
        self.renderfunc = render_template
        self.db = app.db
        self.redirectFunc = redirect
        self.urlfor = url_for

        self.allowedFileExtension = UPLOAD_EXTENSIONS
        self.fileUploadFolder = app.app.config['MOPED_UPLOAD_FOLDER']

        self.session = current_session

        super().__init__(UPLOAD_EXTENSIONS)


    
    def userError(self, **kwargs):
        # render error page with http code 400
        # when called.
        return self.renderfunc(
            'errors/error_base.html',
            **kwargs
        ), 400

    # function for processing moped creation
    def process_create_moped(self, form, files):

        # make sure that all mandatory fields are
        # included in the form & user is authenticated

        mandatoryFields = [
            'brand',
            'model',
            'model_year',
            'description'
        ]

        for field in mandatoryFields:
            if form.get(field) == None or form.get(field) == '' \
                or 'object' not in self.session:
                
                return self.userError(
                    title='Et antanut pakollisia tietoja!',
                    message="Tsekkaahan antamasi tiedot."
                )
            else:
                print(form.get(field))

        # make sure that there is atleast one image

        if 'file' not in files:
            return self.userError(
                title='Et antanut kuvaa!',
                message="Kuva on pakollinen, paskainen mopo ei ole tekosyy."
            )
        
        file = files['file']

        if file.filename == '':
            return self.userError(
                title='Ei valittua kuvaa!',
                message='Kuva on pakollinen. Valitse sellainen.'
           )

        # Make sure that filename is secure
        # to prevent injections and save the file.


        if file and self.allowed_file(file.filename):
            
            # add random uuid to file path before saving
            # but keep the file extension (to prevent)
            # file overwriting (by uploading same-called)
            # file many times

            file_filename, file_extension = os.path.splitext(file.filename)

            not_secured_filename = file_filename + generateSomeRandomString() \
                + file_extension
            
            filename = secure_filename(not_secured_filename)
            self.saved_file_filename = filename

            # save file in upload folder.
            file.save(
                os.path.join(self.fileUploadFolder, filename)
            )
        
            # save filename
            self.savedFileName = file.filename
        else:
            return self.userError(
                title='Paska kuva!',
                message='Kuvan täytyy olla oikean muotoinen.'
            )

        # get user id+username based on 'object' session.
        user_obj = self.session['object']
        user_id = get_id_session_obj(user_obj)
        user_name = User.query.filter_by(id=user_id).first().username

        # store image paths in array

        image_list_dict = []
        image_list_dict.append(self.saved_file_filename)

        # convert image_list_dict to json => store in db (as string)

        image_list = json.dumps(image_list_dict)

        # create and return (just created instance of) moped (pass values as argument)
        created_moped = createMopedObject(
            filename=self.savedFileName,
            db=self.db,
            uname=user_name,
            brand=form.get('brand'),
            model=form.get('model'),
            model_y=form.get('model_year'),
            image_list_json=image_list,
            moped_description=form.get('description')
        )

        # return user to the moped's page

        return self.redirectFunc(
            self.urlfor('moped.view', id=created_moped.id)
        )
    
def createMopedObject(filename, db, uname, brand,\
    model, model_y, image_list_json, moped_description):

    # create new object+commit it to the db and return the object

    current_moped = Moped(
        owner_username=uname,
        brand=brand,
        model=model,
        model_year=model_y,
        image_list=image_list_json,
        description=moped_description
    )


    db.session.add(current_moped)
    db.session.commit()

    return current_moped


