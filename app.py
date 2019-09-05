import markdown
import quart
from quart import Quart

import user_content
from storage import JSONThingStorage

app = Quart(__name__)
app.jinja_env.globals.update(md=markdown.markdown)
post_storage = JSONThingStorage("interim-posts.json")
comments_storage = JSONThingStorage("interim-comments.json")


@app.route("/")
async def front_page():
    newest = sorted(post_storage.items(), key=lambda x: x[1]["timestamp"])[:10]
    return await quart.render_template("front_page.html", pageposts=newest)


@app.route("/post/")
@app.route("/post/<id_>")
async def get_post(id_: str = None):
    if id_ is None:
        return quart.redirect("/")
    try:
        loaded = post_storage[id_]
    except KeyError:
        return quart.Response("404", status=404)
    pos = user_content.Post.deserialize(loaded, id_)
    # load comments from storage
    comments = [
        user_content.Comment.deserialize(v, k)
        for k, v in comments_storage.items()
        if v["parent"] == pos.id
    ]
    return await quart.render_template(
        "post.html",
        title=pos.title,
        content=pos.content,
        comments=comments,
        children_of=comment_children,
    )


def comment_children(c: user_content.Comment):
    return [
        user_content.Comment.deserialize(v, k)
        for k, v in comments_storage.items()
        if k in c.children()
    ]


if __name__ == "__main__":
    app.run()
