from abc import ABC

from ..base import ClientMixin

try:
    import google.auth
    from google.auth.credentials import Credentials
except ImportError:
    raise ImportError("To use the GCP resolvers, you need to: `pip install omegaconf_cloud_resolvers[gcp]`")


class GCPMixin(ClientMixin, ABC):
    """
    Mixin to handle the auth configuration for GCP
    """

    def __init__(self, credentials: Credentials = None, project_id: str = None, *args, **kwargs):
        if credentials is None or project_id is None:
            credentials_, project_id_ = google.auth.default(*args, **kwargs)
        else:
            credentials_, project_id_ = None, None
        self._credentials = credentials or credentials_
        self._project_id = project_id or project_id_
        self.client = self.get_client()
