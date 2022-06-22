from flask import Flask, render_template, session
from user.user import user
from datahandling import dataHandler

# Get 'object' from (client side) session. Will return user_id.
# If it doesn't exist, then the wil return None -object. 

def get_user_session(current_session):
    if 'object' in current_session:
        session = current_session['object']
        
        return session['user_id']