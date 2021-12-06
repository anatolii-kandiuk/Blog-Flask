from flask import Blueprint

personal_computers = Blueprint('pc', __name__, template_folder="templates")

from . import views