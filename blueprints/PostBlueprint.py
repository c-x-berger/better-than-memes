from flask import Blueprint

post_blueprint = Blueprint("post", __name__)


@post_blueprint.route("/content")
def contents():
    return ""
