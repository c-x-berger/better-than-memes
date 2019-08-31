import time

from things import Thing


class Post(Thing):
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

    def serialize(self) -> dict:
        return {
            "author": self.author,
            "timestamp": self.timestamp,
            "content": self.content,
            "title": self.title,
        }

    @staticmethod
    def deserialize(serialized: dict):
        return Post(**serialized)
