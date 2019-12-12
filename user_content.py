from abc import ABC
from datetime import datetime, timezone
from typing import List, Coroutine

import postgres
from things import Thing


class UserContent(Thing, ABC):
    def __init__(
        self,
        author: str,
        content: str,
        timestamp: datetime = datetime.utcnow(),
        id_=None,
    ):
        self.author, self.content, self.timestamp, self._id = (
            author,
            content,
            timestamp,
            id_,
        )

    def serialize(self) -> dict:
        return {
            "author": self.author,
            "timestamp": self.timestamp.replace(tzinfo=timezone.utc).timestamp(),
            "content": self.content,
        }


class Post(UserContent):
    def __init__(
        self,
        author: str,
        title: str,
        board: str,
        content: str = "",
        timestamp: datetime = datetime.utcnow(),
        id_=None,
    ):
        super().__init__(author, content, timestamp, id_)
        self.title = title
        self.board = board

    def serialize(self) -> dict:
        values = super().serialize()
        values.update({"title": self.title, "board": self.board})
        return values

    @staticmethod
    def deserialize(serialized: dict, orig_id: str):
        return Post(**serialized, id_=orig_id)

    @staticmethod
    async def retrieve(id_: str) -> "Post":
        record = await postgres.pool.fetchrow("SELECT * FROM posts WHERE id = $1", id_)
        return Post(
            author=record["author"],
            title=record["title"],
            board=record["board"],
            timestamp=record["timestamp"],
            content=record["content"],
            id_=record["id"],
        )


class Comment(UserContent):
    def __init__(
        self,
        author: str,
        content: str,
        parent: str,
        timestamp: datetime = datetime.utcnow(),
        id_: str = None,
    ):
        super().__init__(author, content, timestamp, id_)
        self.parent = parent

    @property
    def id(self):
        if not self._id:
            # this call to super().id hashes, and we then assign the internal value
            # to avoid that in the future
            self._id = "{}.{}".format(self.parent, super().id)
        return super().id

    def serialize(self) -> dict:
        values = super().serialize()
        values.update({"parent": self.parent})
        return values

    async def children(self) -> Coroutine[List["Comment"]]:
        ids = await postgres.pool.fetch(
            "SELECT id FROM comments WHERE id <@ $1 AND id != $1", self.id
        )
        ret = []
        for row in ids:
            ret.append(await Comment.retrieve(row["id"]))
        return ret

    @staticmethod
    def deserialize(serialized: dict, orig_id: str):
        return Comment(**serialized, id_=orig_id)

    @staticmethod
    async def retrieve(id_: str) -> "Comment":
        record = await postgres.pool.fetchrow(
            "SELECT * FROM comments WHERE id = $1", id_
        )
        return Comment(
            author=record["author"],
            content=record["content"],
            parent=".".join(record["id"].split(".")[:-1]),
            timestamp=record["timestamp"],
            id_=record["id"],
        )
