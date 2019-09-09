import quart
from quart import Blueprint, g

import postgres

post_blueprint = Blueprint("post", __name__)


@post_blueprint.url_value_preprocessor
async def preprocess(_, values):
    g.id_ = values.pop["post_id"]


@post_blueprint.route("/")
async def main_view(post_id=None):
    # load post
    post = await postgres.get_post(post_id)
    comments = await postgres.pool.fetch(
        "SELECT * FROM comments WHERE parent = $1", post_id
    )
    return await quart.render_template(
        "post.html", post=post, comments=comments, children_of=comment_children
    )


@post_blueprint.route("/api/content")
async def contents():
    conts = await postgres.pool.fetchrow(
        "SELECT content FROM posts WHERE id = $1", g.id_
    )
    return conts["contents"]


async def comment_children(parent: str):
    return await postgres.pool.fetch("SELECT * FROM comments WHERE parent = $1", parent)
