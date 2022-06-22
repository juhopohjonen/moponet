# blueprint for moped specific actions.

from flask import Blueprint, redirect, render_template, session, request, url_for
from restrictViews import render_restricted
from sqlalchemy import desc

import models
import json


moped = Blueprint(name='moped', import_name=__name__, url_prefix='/moped',
template_folder='templates', static_folder='mopedstatic')


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
        title='Rekisteröi mopo'
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
        

@moped.route('/view')
@moped.route('/view/')
def view_list():

    # render 30 moped objects server side and
    # more asyncronoysly (via xmlhttprequest)
    # with JavaScript.

    raw_moped_objects = models.Moped.query.order_by(
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
        'moped_list.html',
        title="Selaa mopoja",
        mopeds=moped_list
    )



# Query db and return moped info
# to user
@moped.route('/view/specific/<int:id>')
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
            firstfile=url_for('imagepoint', name=first_file),
            
            # related data = likes & commments
            related_data=requested_moped.get_related_data(),
            title=f'Vuoden {requested_moped.model_year} {requested_moped.brand} {requested_moped.model}',
            
        )