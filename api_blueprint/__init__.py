from datetime import timezone

from quart import Blueprint

import postgres

api = Blueprint("api", __name__)


@api.route("/post/<id_>")
async def get_whole_post(id_: str):
    post = await postgres.get_post(id_)
    ret = {k: v for k, v in post.items()}
    ret["timestamp"] = ret["timestamp"].replace(tzinfo=timezone.utc).timestamp()
    return ret
