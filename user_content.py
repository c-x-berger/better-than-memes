from abc import ABC
from datetime import datetime, timezone
from typing import List

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
        children: List[str] = None,
        timestamp: datetime = datetime.utcnow(),
        id_: str = None,
    ):
        super().__init__(author, content, timestamp, id_)
        self.parent = parent
        if children is None:
            children = []
        self.kids = children

    @property
    def id(self):
        orig_id = super().id
        return "{}.{}".format(self.parent, orig_id)

    def children(self) -> List[str]:
        return self.kids

    def add_child(self, kid: "Comment"):
        self.kids.append(kid.id)

    def serialize(self) -> dict:
        values = super().serialize()
        values.update({"children": self.children(), "parent": self.parent})
        return values

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
