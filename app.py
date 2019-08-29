import json

import flask
from flask import Flask
from jinja2_markdown import MarkdownExtension

import post

app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)
with open("interim-posts.json") as f:
    posts = json.load(f)


@app.route("/")
def hello_world():
    return flask.render_template("blank.html")


@app.route("/post/")
@app.route("/post/<id_>")
def get_post(id_: str = None):
    if id_ is None:
        return flask.redirect("/", code=302)
    try:
        loaded = posts[id_]
    except KeyError:
        return flask.Response(status=404)
    pos = post.Post.deserialize(loaded)
    return flask.render_template("post.html", title=pos.title, content=pos.content)


if __name__ == "__main__":
    app.run()
