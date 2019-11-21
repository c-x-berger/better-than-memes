import flask_login
import quart

import postgres
from . import blue


@blue.route("/<board>")
async def show_board(board: str):
    newest = await postgres.pool.fetch(
        "SELECT * FROM posts WHERE board <@ $1 ORDER BY timestamp DESC LIMIT 25", board
    )
    return await quart.render_template(
        "board/board.html", board=board, pageposts=newest
    )


@blue.route("/create", ["GET", "POST"])
@flask_login.login_required
async def create_board():
    if quart.request.method == "GET":
        return await quart.render_template("board/creation.html")

    try:
        path: str = (await quart.request.form)["path"].lower()
    except KeyError:
        await quart.flash("no board given")
        return await quart.render_template("board/creation.html")
    # we need a != because the descendant operator sucks
    viable_child = await postgres.pool.fetchrow(
        "SELECT * FROM boards WHERE $1 <@ path AND $1 != path LIMIT 1", path
    )
    if viable_child is not None:
        await postgres.pool.execute(
            "INSERT INTO boards (path, creator) VALUES ($1, $2)",
            path,
            flask_login.current_user.id,
        )
        return quart.redirect(quart.url_for("board.show_board", board=path))
