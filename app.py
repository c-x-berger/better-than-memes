from datetime import timezone

import markdown
import quart
import quart.flask_patch
from quart import Quart

import config
import login
import postgres
import user
from api_blueprint import api
from post.post import post_blueprint

app = Quart(__name__)
app.jinja_env.globals.update(md=markdown.markdown)
app.jinja_env.globals.update(
    nix_time=lambda dt: dt.replace(tzinfo=timezone.utc).timestamp()
)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = config.SECRET_KEY
login.login_man.init_app(app)


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
app.register_blueprint(login.blue, "/")
app.register_blueprint(user.blue, "/user/<user>")
# API MUST BE LAST
app.register_blueprint(api, "/api")

if __name__ == "__main__":
    app.run()
