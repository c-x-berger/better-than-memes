import bleach
import flask_login
import markdown
from quart import request

import config
import postgres
from blueprints.api import blue
from user_content import Comment


@blue.route("/add-comment", ["POST"])
@flask_login.login_required
async def add_comment():
    """
    Add a comment. HTTP JSON API.
    Parameters:
    - content (str): Markdown string of content
    - parent (id): ID of Thing being replied to
    :return: JSON with status and possibly the HTML render of content
    """
    data = await request.get_json()
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
    else:
        return {"status": "not-ok", "reason": "send JSON next time you fool"}, 400


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
