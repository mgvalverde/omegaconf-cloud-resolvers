from abc import ABC, abstractmethod
from typing import Union, List, Dict

JsonType = Union[None, int, str, bool, List["JsonType"], Dict[str, "JsonType"]]


class PluginResolver(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        # The retriever uses a callable, don't want to restrict the argument format
        pass


class ClientMixin(ABC):
    client: any  # TODO: assign a valid type from a valid cloud provider

    @abstractmethod
    def get_client(self):
        pass
