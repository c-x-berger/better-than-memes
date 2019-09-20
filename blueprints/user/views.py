import quart

import postgres
from blueprints.user import blue


@blue.route("/")
async def user_overview(user: str = None):
    posts = await postgres.pool.fetch(
        "SELECT id, author, title, timestamp FROM posts WHERE author = $1 ORDER BY timestamp DESC LIMIT 25",
        user,
    )
    post_count = len(posts)
    comments = await postgres.pool.fetch(
        "SELECT content, timestamp, post FROM comments WHERE author = $1 ORDER BY timestamp DESC LIMIT 25",
        user,
    )
    comment_count = len(comments)

    content = [
        {
            "id": post["id"],
            "title": post["title"],
            "timestamp": post["timestamp"],
            "type": "post",
        }
        for post in posts
    ]
    content += [
        {
            "content": comment["content"],
            "timestamp": comment["timestamp"],
            "post": comment["post"],
            "post_title": (
                await postgres.pool.fetchrow(
                    "SELECT title FROM posts WHERE id = $1", comment["post"]
                )
            )["title"],
            "type": "comment",
        }
        for comment in comments
    ]
    content = sorted(content, key=lambda k: k["timestamp"])[:25]

    return await quart.render_template(
        "user_overview.html",
        username=user,
        posts=post_count,
        comments=comment_count,
        content=content,
    )
