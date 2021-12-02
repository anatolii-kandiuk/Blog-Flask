from flask import Blueprint

form = Blueprint('forms', __name__, template_folder="templates")

from . import views