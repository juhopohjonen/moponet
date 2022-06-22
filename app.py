
import os, json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect



# Get path of this directory
FILE_DIRECTORY_LOCATION = os.path.dirname(os.path.realpath(__file__))


# get path & contents of config.json file
CONFIG_FILENAME = 'config.json'
CONFIG_FILEPATH = os.path.join(FILE_DIRECTORY_LOCATION, CONFIG_FILENAME)


with open(CONFIG_FILEPATH) as config_file:
    configuration = json.load(config_file)


# Set URI of your database here (refer to flask_sqlalchemy docs for help)
DB_PATH = ''


# Development server variables
DEBUG_MODE = True
SERVER_PORT = 80


# Create mandatory instances & adjulst db+application configuration
app = Flask(__name__)

db = SQLAlchemy(app)
from models import *


# register blueprints
from moped.moped import moped
from user import user

user_bp = user.user

app.register_blueprint(moped)
app.register_blueprint(user_bp)

# configure secret key
app.config['SECRET_KEY'] = configuration["SECRET_KEY"]


# Configure app ( based on config.json )
upload_config = configuration["UPLOADS"]
app.config['UPLOAD_FOLDER'] = upload_config["UPLOAD_FOLDER_PATH"]
UPLOAD_EXTENSIONS = upload_config["ALLOWED_EXTENSIONS"]


# Initialize Cross-Site Request Forgery protection
csrf = CSRFProtect()
csrf.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH



# Import modules
from views import *


if __name__ == '__main__':
    app.run(debug=DEBUG_MODE, port=SERVER_PORT)

