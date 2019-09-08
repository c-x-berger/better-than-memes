import markdown
import quart
from quart import Quart

import postgres
from blueprints.PostBlueprint import post_blueprint
from storage import JSONThingStorage

app = Quart(__name__)
app.jinja_env.globals.update(md=markdown.markdown)
post_storage = JSONThingStorage("interim-posts.json")
comments_storage = JSONThingStorage("interim-comments.json")


@app.route("/")
async def front_page():
    newest = sorted(post_storage.items(), key=lambda x: x[1]["timestamp"])[:10]
    return await quart.render_template("front_page.html", pageposts=newest)


@app.before_first_request
async def init():
    await postgres.init_pool()


app.register_blueprint(post_blueprint, "/post/<post_id>")

if __name__ == "__main__":
    app.run()
