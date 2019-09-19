from quart import Blueprint

blue = Blueprint("user", __name__)

from . import views
