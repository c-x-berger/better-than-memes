import abc
import json
from typing import Optional

from things import Thing


class ThingStorage(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, item: str) -> Optional[dict]:
        """
        Return a serialized Thing of ID `item`.
        :param item: The ID to retrieve
        :return: Serialized Thing, or None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, key: str, value: Thing):
        """
        Store a Thing at the given key (usually the Thing's ID.)

        While specifying None as the key is legal, this will store the Thing at it's computed ID and may cause
        unexpected behavior.
        :param key: The key to store the thing at.
        :param value: The serialized thing to store.
        """
        raise NotImplementedError


class JSONThingStorage(ThingStorage):
    # TODO: SQL storage
    def __init__(self, filename: str):
        self.filename = filename
        with open(filename, "r") as f:
            self.data = json.load(f)

    def items(self):
        return self.data.items()

    def __getitem__(self, item: str) -> Optional[dict]:
        try:
            return self.data[item]
        except KeyError:
            return None

    def __setitem__(self, key: str, value: Thing):
        self.data[key] = value.serialize()

    def __del__(self):
        # hopefully this runs when we go out
        # otherwise I'm screwed
        with open(self.filename, "w") as f:
            json.dump(self.data, f)
