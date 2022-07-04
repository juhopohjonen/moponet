# Module for moped meetings

from flask import Flask, Blueprint

meets = Blueprint(
    'meets',
    __name__,
    static_folder='meetstatic',
    template_folder='meetstemplates',
    url_prefix='/meets'
)

from meets.views import *
from meets.handling import *