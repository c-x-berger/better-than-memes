import datetime

import bleach
import flask_login
import markdown
import quart

import config
import postgres
from blueprints.api import blue
from user_content import Comment


@blue.route("/add-comment", ["POST"])
@flask_login.login_required
async def add_comment():
    data = await quart.request.json
    if data is not None:
        content = data["content"]
        try:
            parent = data["parent"]
        except KeyError:
            return (
                {
                    "status": "not-ok",
                    "reason": "no parent supplied - give parent comment or post id",
                },
                400,
            )
        c = Comment(flask_login.current_user.id, content, parent)
        await postgres.pool.execute(
            "INSERT INTO comments(id, author, timestamp, content) VALUES ($1, $2, $3, $4)",
            c.id,
            c.author,
            c.timestamp,
            content,
        )
        return {
            "status": "ok",
            "rendered": bleach.clean(
                markdown.markdown(content, extensions=config.MARKDOWN_EXTENSIONS),
                tags=config.ALLOWED_HTML,
            ),
        }


@blue.route("/comment-html/<id_>")
async def comment_html(id_: str):
    contents = (await postgres.get_comment(id_))["content"]
    return {
        "status": "ok",
        "rendered": bleach.clean(
            markdown.markdown(contents, extensions=config.MARKDOWN_EXTENSIONS),
            tags=config.ALLOWED_HTML,
        ),
    }
