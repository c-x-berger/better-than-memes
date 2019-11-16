import datetime
from datetime import timezone

import flask_login
import quart
from asyncpg import UniqueViolationError, ForeignKeyViolationError
from quart import request

import postgres
from blueprints import api
from blueprints.post import blue
from user_content import Post


@blue.route("/<post_id>")
async def main_view(post_id=None):
    post = await postgres.get_post(post_id)
    if post is None:
        return "not found", 404
    comments = await postgres.pool.fetch(
        "SELECT * FROM comments WHERE id ~ ($1 || '.*{1}')::lquery", post_id
    )
    return await quart.render_template(
        "post/post.html", post=post, comments=comments, children_of=comment_children
    )


@blue.route("/submit", ["GET", "POST"])
@flask_login.login_required
async def submit_page():
    if request.method == "GET":
        return await quart.render_template("post/submit.html")

    try:
        contents = (await request.form)["text"]
    except KeyError:
        contents = ""
    try:
        title = (await request.form)["title"]
    except KeyError:
        await quart.flash("no title")
        return await quart.render_template("post/submit.html")
    try:
        board = (await request.form)["board"]
    except KeyError:
        await quart.flash("no board")
        return await quart.render_template("post/submit.html")
    user = flask_login.current_user.id
    p = Post(user, title, board, content=contents)
    try:
        await postgres.pool.execute(
            "INSERT INTO posts(id, title, author, content, timestamp, board) VALUES ($1, $2, $3, $4, $5, $6)",
            p.id,
            p.title,
            p.author,
            p.content,
            datetime.date.fromtimestamp(p.timestamp),
            p.board,
        )
    except ForeignKeyViolationError:
        await quart.flash("board <code>{}</code> does not exist".format(board))
        return await quart.render_template("post/submit.html")
    except UniqueViolationError:
        await quart.flash("bruh moment, yell at c-x-berger")
        return await quart.render_template("post/submit.html")
    else:
        return quart.redirect(quart.url_for("post.main_view", post_id=p.id))


@api.blue.route("/post/<id_>/")
async def get_whole_post(id_: str):
    post = await postgres.get_post(id_)
    ret = {k: v for k, v in post.items()}
    ret["timestamp"] = ret["timestamp"].replace(tzinfo=timezone.utc).timestamp()
    return ret


async def comment_children(parent: dict):
    return await postgres.pool.fetch(
        "SELECT * FROM comments WHERE id ~ ($1 || '.*{1}')::lquery ORDER BY timestamp DESC", parent["id"]
    )
