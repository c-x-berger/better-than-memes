import asyncio

import flask_bcrypt
from flask_login import UserMixin

import postgres
from . import login_man


class User(UserMixin):
    def __init__(self, username: str, auth: bool = False):
        self.id = username
        self._auth = auth

    @property
    def is_authenticated(self):
        return self._auth

    @is_authenticated.setter
    def is_authenticated(self, auth: bool):
        self._auth = auth


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
    if not user:
        return
    u = User(username)
    u.is_authenticated = flask_bcrypt.check_password_hash(user["password"], password)
    return u


@login_man.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized"
