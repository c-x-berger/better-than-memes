import abc
import hashlib
import json


class Thing(abc.ABC):
    @property
    def id(self):
        j = json.dumps(self.serialized)
        return hashlib.sha256(j.encode("utf-8")).hexdigest()

    @property
    def short_id(self):
        return self.id[:7]

    @property
    @abc.abstractmethod
    def serialized(self):
        """
        Serialize this Thing as a dictionary. Should be suitable for JSON dumping.
        Update your parent class' serialize method as opposed to overloading to avoid Boilerplate(tm).

        :return: This Thing, serialized to a JSON-suitable dictionary.
        """
        ...

    @staticmethod
    @abc.abstractmethod
    def deserialize(serialized: dict):
        """
        Reconstitute a Thing from its dictionary form.
        :param serialized: The serialized Thing
        :return: A deserialized Thing
        """
        ...
