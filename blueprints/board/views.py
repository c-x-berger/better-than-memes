import quart

import postgres
from . import blue


@blue.route("/<board>")
async def show_board(board: str):
    newest = await postgres.pool.fetch(
        "SELECT * FROM posts WHERE board <@ $1 ORDER BY timestamp DESC LIMIT 25", board
    )
    return await quart.render_template("front_page.html", pageposts=newest)
