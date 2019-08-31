import flask
from flask import Flask
from jinja2_markdown import MarkdownExtension

import user_content
from storage import JSONThingStorage

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)
post_storage = JSONThingStorage("interim-posts.json")
comments_storage = JSONThingStorage("interim-comments.json")


@app.route("/")
def front_page():
    newest = sorted(post_storage.items(), key=lambda x: x[1]["timestamp"])[:10]
    return flask.render_template("front_page.html", pageposts=newest)


@app.route("/post/")
@app.route("/post/<id_>")
def get_post(id_: str = None):
    if id_ is None:
        return flask.redirect("/", code=302)
    try:
        loaded = post_storage[id_]
    except KeyError:
        return flask.Response(status=404)
    pos = user_content.Post.deserialize(loaded, id_)
    return flask.render_template("post.html", title=pos.title, content=pos.content)


if __name__ == "__main__":
    app.run()
