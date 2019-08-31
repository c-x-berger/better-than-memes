import time
from abc import ABC
from typing import List

from things import Thing


class UserContent(Thing, ABC):
    def __init__(self, author: str, content: str, timestamp: float = time.time(), id_=None):
        self.author, self.content, self.timestamp, self._id = author, content, timestamp, id_

    def serialize(self) -> dict:
        return {
            "author": self.author,
            "timestamp": self.timestamp,
            "content": self.content,
        }


class Post(UserContent):
    def __init__(
        self, author: str, title: str, content: str = "", timestamp: float = time.time(), id_=None
    ):
        super().__init__(author, content, timestamp, id_)
        self.title = title

    def serialize(self) -> dict:
        values = super().serialize()
        values.update({"title": self.title})
        return values

    @staticmethod
    def deserialize(serialized: dict, orig_id: str):
        return Post(**serialized, id_=orig_id)


class Comment(UserContent):
    def __init__(
        self,
        author: str,
        content: str,
        parent: str,
        children=None,
        timestamp: float = time.time(),
        id_=None
    ):
        super().__init__(author, content, timestamp, id_)
        self.parent = parent
        if children is None:
            children = []
        self.kids = children

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
