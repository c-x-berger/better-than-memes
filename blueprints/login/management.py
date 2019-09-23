import asyncio

import flask_bcrypt
from flask_login import UserMixin

import postgres
from . import login_man


class User(UserMixin):
    def __init__(self, username: str):
        self.id = username


@login_man.user_loader
def user_loader(username: str):
    user = asyncio.get_event_loop().sync_wait(
        postgres.pool.fetchrow(
            "SELECT username FROM users WHERE username = $1", username
        )
    )
    if user["username"]:
        return User(user["username"])
    else:
        return None


@login_man.request_loader
def request_loader(req):
    username = req.form.get("username")
    password = req.form.get("password", "")
    user = asyncio.get_event_loop().sync_wait(
        postgres.pool.fetchrow(
            "SELECT username, password FROM users WHERE username = $1", username
        )
    )
    if not user or not flask_bcrypt.check_password_hash(user["password"], password):
        return
    u = User(username)
    return u


@login_man.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized"
