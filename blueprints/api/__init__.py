from quart import Blueprint

blue = Blueprint("api", __name__)

from . import commenting
