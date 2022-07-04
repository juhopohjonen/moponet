# Views (url routings) for moped meets

from flask import Flask, redirect, render_template, request, url_for
from meets.meets import meets
import meets.handling as handling


# Function for viewing list of moped meets
@meets.route('/')
def view_list():
    return render_template(
        'viewlist.html',
        title="Selaa mopomiittejä"
    )


# View specific meet with id (query param 'meet')
@meets.route('/viewmeet')
def view():
    args_id = request.args.get('meet')

    # try to convert args_id to str
    # if cannot: redirect to list & status 400

    try:
        meet_id = int(args_id)
    except:
        return redirect(url_for('meets.view_list')), 400

    return handling.viewmeet(meet_id)


# View 'organize meet' page
@meets.route('/organize')
def organize():
    return render_template(
        'organize_meet.html',
        title='Järjestä mopomiitti'
    )