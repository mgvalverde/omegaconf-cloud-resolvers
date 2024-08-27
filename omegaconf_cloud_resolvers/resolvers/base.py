from abc import ABC, abstractmethod


class Resolver(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        # The retriever uses a callable
        pass


class ClientMixin(ABC):
    client: any  # TODO: assign a valid type from a valid cloud provider

    @abstractmethod
    def get_client(self):
        pass
