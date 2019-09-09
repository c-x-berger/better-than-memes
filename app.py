from datetime import timezone

import markdown
import quart
from quart import Quart

import postgres
from post.post import post_blueprint

app = Quart(__name__)
app.jinja_env.globals.update(md=markdown.markdown)
app.jinja_env.globals.update(
    nix_time=lambda dt: dt.replace(tzinfo=timezone.utc).timestamp()
)


@app.route("/")
async def front_page():
    newest = await postgres.pool.fetch(
        "SELECT * FROM posts ORDER BY timestamp LIMIT 10"
    )
    return await quart.render_template("front_page.html", pageposts=newest)


@app.before_serving
async def init():
    await postgres.init_pool()


app.register_blueprint(post_blueprint, "/post/<post_id>")

if __name__ == "__main__":
    app.run()
