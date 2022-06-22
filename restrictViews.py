# login management extension with restricting views
# written by me, because i got some problems with
# flask-login, so i decided to re-write it with
# more familiar API for me.

from flask import render_template, session
import uuid

# Set flask session's object name HERE.
SESSION_OBJECT_NAME = 'object'


# Error message values
ERROR_MESSAGE_TITLE = "Vain kirjautuneille!"
ERROR_MESSAGE_BODY = "Vain kirjautuneet voivat käyttää tätä sivua."

# Set render function (don't call it)
RENDER_FUNCTION = render_template


# Restricted page function returned when user tries to
# view restricted pages


def restrictedPage():
    return render_template(
        template_name_or_list='errors/restricted.html',
        title=ERROR_MESSAGE_TITLE,
        message=ERROR_MESSAGE_BODY
    )


def render_restricted(session, **kwargs):
    # check if user is not signed in
    # if signed in => return restrict page error

    if SESSION_OBJECT_NAME not in session:
        return restrictedPage(), 400

    return RENDER_FUNCTION(**kwargs)


# Generate random uuid => return as str
def generateSomeRandomString():
    unique_id = uuid.uuid4()
    return str(unique_id)