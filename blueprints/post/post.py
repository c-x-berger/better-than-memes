from datetime import timezone

import flask_login
import quart
from quart import request

import postgres
from blueprints import api
from blueprints.post import blue


@blue.route("/<post_id>")
async def main_view(post_id=None):
    post = await postgres.get_post(post_id)
    comments = await postgres.pool.fetch(
        "SELECT * FROM comments WHERE parent = $1", post_id
    )
    return await quart.render_template(
        "post/post.html", post=post, comments=comments, children_of=comment_children
    )


@blue.route("/submit", ["GET", "POST"])
@flask_login.login_required
async def submit_page():
    if request.method == "GET":
        return "yare yare daze"

    contents = (await request.form)["text"]
    title = (await request.form)["title"]


@api.blue.route("/post/<id_>/")
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
