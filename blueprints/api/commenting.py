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
            parent = ""
        try:
            if parent != "":
                post = (await postgres.get_comment(parent))["post"]
            else:
                # KeyError could happen here
                post = data["post"]
                parent = post
        except KeyError:
            return "no post could be found - give parent comment or post id", 400
        c = Comment(flask_login.current_user.id, content, parent)
        await postgres.pool.execute(
            "INSERT INTO comments(id, author, timestamp, parent, post, content) VALUES ($1, $2, $3, $4, $5, $6)",
            c.id,
            c.author,
            datetime.date.fromtimestamp(c.timestamp),
            parent,
            post,
            content,
        )
        return bleach.clean(
            markdown.markdown(content, extensions=config.MARKDOWN_EXTENSIONS),
            tags=config.ALLOWED_HTML,
        )


@blue.route("/comment-html/<id_>")
async def comment_html(id_: str):
    contents = (await postgres.get_comment(id_))["content"]
    return bleach.clean(
        markdown.markdown(contents, extensions=config.MARKDOWN_EXTENSIONS),
        tags=config.ALLOWED_HTML,
    )
