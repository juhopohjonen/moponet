# blueprint for moped specific actions.

from flask import Blueprint, redirect, render_template, session, request, url_for    
from restrictViews import render_restricted
from sqlalchemy import desc

import models
import json

from user.userhandling import get_uid_by_session
import datahandling

moped = Blueprint(name='moped', import_name=__name__, url_prefix='/moped',
template_folder='mopedtemplates', static_folder='mopedstatic')


# import API's
from moped.apis import *


@moped.route('/register', methods=["GET", "POST"])
def register():

    # does user want to GET register form 
    # or POST (create) new moped object? (to db) ?


    if request.method == "GET":

        return render_restricted(session,
        template_name_or_list='register_moped_page.html',
        template_folder=moped.template_folder,
        title='Lisää moposi'
        )
    elif request.method == "POST":

        
        # Import and create mopedDataHandler object

        from moped.moped_datahandling import mopedDataHandler
        dataHandler = mopedDataHandler(current_session=session)


        # Get (rendered, as string) template from process_create_moped func
        # and destroy the object.
        created_moped = dataHandler.process_create_moped(
            form=request.form,
            files=request.files
        )
        del dataHandler


        return created_moped
        

@moped.route('/')
def view_list():

    object_limit = app.configuration["RENDERED_MOPED_OBJECTS"]

    # render 20 moped objects if in database (descending)
    # take 'start' query param for filtering objects
 
    if request.args.get('start') != None:
        try:
            start = int(request.args.get('start'))
        except:
            abort(400)


        all_objs = models.Moped.query.order_by(
            models.Moped.id.desc()).all()
        
        print(f'all objs len: {len(all_objs)}')

        raw_moped_objects = []

        for obj in all_objs:
            if len(raw_moped_objects) >= object_limit:
                break

            if all_objs.index(obj) + 2 > start:
                raw_moped_objects.append(obj)
    else:
        raw_moped_objects = models.Moped.query.order_by(
            models.Moped.id.desc()
            ).limit(object_limit).all(
        )

        start = 0

    moped_list = []
    # return mopeds as moped_content dir
    # which contains also related data
    # eg. photos, likes, comments

    last_moped = 0
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
        'moped_list.html',
        title="Selaa mopoja",
        mopeds=moped_list,
        fetchMopedURL = url_for('moped.fetch_mopeds_api'),
        startvalue=start
    )



# Query db and return moped info
# to user
@moped.route('/<int:id>')
def view(id):
    # import moped model
    from models import Moped
    from app import app
    from views import download_file


    # query the database
    requested_moped = Moped.query.filter_by(
        id=id
    ).first_or_404()

    
    # Convert json column of
    # requested_moped to obj
    image_list = requested_moped.json2list()
    first_file = image_list[0]


    return render_template(
        'view_moped.html',
            moped=requested_moped,
            firstfile=url_for('moped.mopedimages', name=first_file),
            
            # related data = likes & commments
            related_data=requested_moped.get_related_data(),
            title=f'Vuoden {requested_moped.model_year} {requested_moped.brand} {requested_moped.model}',
            
            # url's for like apis
            likeStatusAPI=url_for('moped.like_status_api', mopedid=requested_moped.id),
            LikeApi=url_for('moped.changeLike', mopedid=requested_moped.id)

        )

# return public moped images when called
@moped.route('/mopedimages/<name>')
def mopedimages(name):
    return datahandling.download_file(name, app.app.config["MOPED_UPLOAD_FOLDER"])