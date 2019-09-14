from datetime import timezone

import markdown
import quart
import quart.flask_patch
from flask_login import LoginManager
from quart import Quart

import postgres
from api_blueprint import api
from login.user import User
from post.post import post_blueprint

app = Quart(__name__)
app.jinja_env.globals.update(md=markdown.markdown)
app.jinja_env.globals.update(
    nix_time=lambda dt: dt.replace(tzinfo=timezone.utc).timestamp()
)
login_man = LoginManager()
login_man.init_app(app)


@app.route("/")
async def front_page():
    newest = await postgres.pool.fetch(
        "SELECT * FROM posts ORDER BY timestamp LIMIT 10"
    )
    return await quart.render_template("front_page.html", pageposts=newest)


@app.before_serving
async def init():
    await postgres.init_pool()


@login_man.user_loader
async def user_loader(username: str):
    user = await postgres.pool.fetchrow(
        "SELECT username FROM users WHERE username = $1", username
    )
    if user["username"]:
        return User(user["username"])
    else:
        return None


app.register_blueprint(post_blueprint, "/post/<post_id>")
app.register_blueprint(api, "/api")

if __name__ == "__main__":
    app.run()
