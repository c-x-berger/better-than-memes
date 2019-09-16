from datetime import timezone

import quart

import postgres
from api_blueprint import api
from post import post_blueprint


@post_blueprint.route("/")
async def main_view(post_id=None):
    post = await postgres.get_post(post_id)
    comments = await postgres.pool.fetch(
        "SELECT * FROM comments WHERE parent = $1", post_id
    )
    return await quart.render_template(
        "post/post.html", post=post, comments=comments, children_of=comment_children
    )


@api.route("/post/<id_>/")
async def get_whole_post(id_: str):
    post = await postgres.get_post(id_)
    ret = {k: v for k, v in post.items()}
    ret["timestamp"] = ret["timestamp"].replace(tzinfo=timezone.utc).timestamp()
    return ret


async def comment_children(parent: dict):
    return await postgres.pool.fetch(
        "SELECT * FROM comments WHERE id = ANY ($1) ORDER BY timestamp DESC",
        parent["children"],
    )
