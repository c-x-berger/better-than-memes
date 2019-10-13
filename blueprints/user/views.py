import flask_login
import quart

import postgres
from blueprints.user import blue


@blue.route("/me")
async def selfpage():
    if not flask_login.current_user.is_anonymous:
        return quart.redirect(
            quart.url_for(".user_overview", user=flask_login.current_user.id)
        )
    return quart.redirect(quart.url_for("login.login"))


@blue.route("/<user>")
async def user_overview(user: str = None):
    content = []
    seen_comments = []
    posts = await postgres.pool.fetch(
        "SELECT * FROM posts WHERE author = $1 ORDER BY timestamp DESC LIMIT 25", user
    )
    post_count = len(posts)
    for post in posts:
        p = {"type": "post"}
        p.update(post)
        replies = await postgres.pool.fetch(
            "SELECT id, content, timestamp FROM comments WHERE post = $1 AND author = $2 ORDER BY timestamp DESC",
            post["id"],
            user,
        )
        seen_comments.extend([c["id"] for c in replies])
        p["comments"] = replies
        content.append(p)
    comments = await postgres.pool.fetch(
        "SELECT content, timestamp, post FROM comments WHERE author = $1 AND NOT id = ANY($2) ORDER BY timestamp DESC LIMIT 25",
        user,
        seen_comments,
    )
    comment_count = len(comments)

    for comment in comments:
        c = {
            "type": "comment",
            "post_title": (
                await postgres.pool.fetchrow(
                    "SELECT title FROM posts WHERE id = $1", comment["post"]
                )
            )["title"],
        }
        c.update(comment)
        content.append(c)
    content = sorted(content, key=lambda k: k["timestamp"], reverse=True)[:25]

    return await quart.render_template(
        "user_overview.html",
        username=user,
        posts=post_count,
        comments=comment_count,
        content=content,
    )
