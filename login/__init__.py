from flask_login import LoginManager
from quart import Blueprint

blue = Blueprint("login", __name__)
login_man = LoginManager()

from . import management, views
