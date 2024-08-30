from abc import ABC

from ..base import ClientMixin

try:
    import boto3
except ImportError:
    raise ImportError("To use the AWS resolvers, you need to: `pip install omegaconf_cloud_resolvers[aws]`")


class AWSMixin(ClientMixin, ABC):
    """
    Mixin to handle the auth configuration for AWS
    """

    def __init__(self, session: boto3.Session = None, *args, **kwargs):
        self._session = session or boto3.Session(*args, **kwargs)
        self.client = self.get_client()
