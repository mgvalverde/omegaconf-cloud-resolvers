from abc import ABC

from ..base import ClientMixin

try:
    from azure.identity import DefaultAzureCredential, ChainedTokenCredential
except ImportError:
    raise ImportError(
        "To use the Microsoft Azure resolvers, you need to: `pip install omegaconf_cloud_resolvers[az]`"
    )


class AzureMixin(ClientMixin, ABC):

    """
    Mixin to handle the auth configuration for Microsoft Azure
    """

    def __init__(self, credentials: ChainedTokenCredential = None, *args, **kwargs):
        self._credentials = credentials or DefaultAzureCredential(*args, **kwargs)
        self.client = self.get_client()
