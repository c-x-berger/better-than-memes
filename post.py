import hashlib
import json
import time


class Post:
    author: str = None
    timestamp: float = None
    content = ""
    title: str

    def __init__(
        self, author: str, title: str, content: str = "", timestamp: float = time.time()
    ):
        self.author, self.title, self.content, self.timestamp = (
            author,
            title,
            content,
            timestamp,
        )

    @property
    def id(self):
        return hashlib.sha256(self.serialized.encode("utf-8")).hexdigest()

    @property
    def short_id(self):
        return self.id[:7]

    @property
    def serialized(self):
        return json.dumps(
            {
                "author": self.author,
                "timestamp": self.timestamp,
                "content": self.content,
                "title": self.title,
            }
        )

    @staticmethod
    def deserialize(serial: str):
        return Post(**json.loads(serial))
