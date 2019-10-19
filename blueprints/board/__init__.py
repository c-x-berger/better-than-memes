from quart import Blueprint

blue = Blueprint("board", __name__)

from . import views
