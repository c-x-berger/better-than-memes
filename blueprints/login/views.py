import flask_bcrypt
import flask_login
import quart
from quart import request

import postgres
from blueprints.login.management import User
from . import blue


@blue.route("login", ["GET", "POST"])
async def login():
    if request.method == "GET":
        if not flask_login.current_user.is_anonymous:
            return quart.redirect(quart.url_for("front_page"))
        return await quart.render_template("login/login.html")

    username = (await request.form)["username"]
    user_rec = await postgres.pool.fetchrow(
        "SELECT username, password FROM users WHERE username = $1", username
    )
    if user_rec:
        if flask_bcrypt.check_password_hash(
            user_rec["password"], (await request.form)["password"]
        ):
            flask_login.login_user(User(username, True))
            return quart.redirect("/")
        await quart.flash("bad password")
        return await quart.render_template("login/login.html"), 401
    await quart.flash("user <code>{}</code> not found".format(username))
    return await quart.render_template("login/login.html"), 401


@blue.route("logout")
async def logout():
    if flask_login.current_user.is_anonymous:
        return quart.redirect("/login")
    else:
        flask_login.logout_user()
        return quart.redirect("/")
