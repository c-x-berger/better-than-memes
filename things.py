import abc
import hashlib
import json

import config


class Thing(abc.ABC):
    _id: str

    @property
    def id(self):
        if not self._id:
            j = json.dumps(self.serialize())
            self._id = hashlib.sha256(j.encode("utf-8")).hexdigest()[: config.ID_LENGTH]
        return self._id

    @abc.abstractmethod
    def serialize(self) -> dict:
        """
        Serialize this Thing as a dictionary. Should be suitable for JSON dumping.
        Update your parent class' serialize method as opposed to overloading to avoid Boilerplate(tm).

        :return: This Thing, serialized to a JSON-suitable dictionary.
        """
        ...

    @staticmethod
    @abc.abstractmethod
    def deserialize(serialized: dict, original_id: str):
        """
        Reconstitute a Thing from its dictionary form and ID calculated at creation.
        :param original_id: The Thing's ID, as calculated prior to any editing
        :param serialized: The serialized Thing
        :return: A deserialized Thing
        """
        ...

    @staticmethod
    @abc.abstractmethod
    async def retrieve(id_: str) -> "Thing":
        """
        Retrieve and return an instance of a Thing from storage by id.
        :param id_: The ID of the Thing to retrieve
        """
        ...
