from flask import Blueprint

api = Blueprint('api', __name__)

from . import category, post, personal_computer