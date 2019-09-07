from quart import Blueprint, g

import postgres

post_blueprint = Blueprint("post", __name__)


@post_blueprint.url_value_preprocessor
async def preprocess(_, values):
    g.id_ = values["post_id"]


@post_blueprint.route("/")
async def main_view():
    id_ = g.id_
    # load post
    post = await postgres.get_post(id_)


@post_blueprint.route("/api/content")
async def contents():
    conts = await postgres.pool.fetchrow(
        "SELECT contents FROM posts WHERE id = $1", g.id_
    )
    return conts["contents"]
