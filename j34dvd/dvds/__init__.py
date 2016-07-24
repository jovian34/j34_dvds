__author__ = 'carljame'

from flask import Blueprint

dvds = Blueprint('dvds', __name__)

from . import views
