from quart import Blueprint

blue = Blueprint("post", __name__)

from . import post
