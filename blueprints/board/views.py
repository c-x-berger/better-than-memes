import bleach
import flask_login
import quart

import postgres
from util import path
from . import blue


@blue.route("/<board>")
async def show_board(board: str):
    board_parts = [p for p in board.split(".") if p != ""]
    sql_ready = []
    for i in range(len(board_parts)):
        part = board_parts[i]
        if part == "*":
            sql_ready.append("*{1}")
        elif part == "**":
            sql_ready.append("*")
        elif part.startswith("_"):
            excludes = part[1:].split(",")
            sql_ready.append("!" + "|".join(excludes))
        else:
            # special cases that happen on last part
            if i == len(board_parts) - 1:
                if part != "-":
                    sql_ready.extend((part, "*"))
            else:
                sql_ready.append(part)
    query = ".".join(sql_ready)
    newest = await postgres.pool.fetch(
        "SELECT * FROM posts WHERE board ~ $1 ORDER BY timestamp DESC LIMIT 25", query
    )
    return await quart.render_template(
        "board/board.html", board=board, pageposts=newest
    )


@blue.route("/create", ["GET", "POST"])
@flask_login.login_required
async def create_board():
    # TODO: prevent names from starting with control characters in show_board
    if quart.request.method == "GET":
        return await quart.render_template("board/creation.html")

    try:
        path_: str = bleach.clean((await quart.request.form)["path"].lower())
    except KeyError:
        await quart.flash("no board given")
        return await quart.render_template("board/creation.html")
    # we need a != because the descendant operator sucks
    viable_child = await postgres.pool.fetchval(
        "SELECT EXISTS(SELECT FROM boards WHERE path = $1)", path_.split(".")[:-1]
    )
    viable_child = viable_child and path.is_valid(path_)
    if viable_child:
        await postgres.pool.execute(
            "INSERT INTO boards (path, creator) VALUES ($1, $2)",
            path_,
            flask_login.current_user.id,
        )
        return quart.redirect(quart.url_for("board.show_board", board=path_))
    else:
        if path.is_valid(path_):
            await quart.flash(
                "{} is not a valid board path (check for illegal chars)".format(path_)
            )
        else:
            await quart.flash("{} is not a child of any existing board".format(path_))
        return await quart.render_template("board/creation.html")


@blue.route("/list")
async def board_list():
    boards_rec = await postgres.pool.fetch(
        "SELECT path FROM boards WHERE path ~ '*{1}'"
    )
    boards = [b["path"] for b in boards_rec]
    return await quart.render_template(
        "board/list.html",
        boards=boards,
        children_of=child_boards,
    )


async def child_boards(board: str):
    return [
        b["path"]
        for b in await postgres.pool.fetch(
            "SELECT path FROM boards WHERE path ~ ($1 || '.*{1}')::lquery and path != text2ltree($1)", board
        )
    ]
