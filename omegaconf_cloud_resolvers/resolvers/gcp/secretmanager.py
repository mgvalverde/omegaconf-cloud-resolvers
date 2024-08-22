from typing import Dict

from .base import GCPMixin
from ..base import Resolver


class GCPSecretManagerMixin(GCPMixin):
    def get_client(self):
        try:
            from google.cloud import secretmanager
        except ImportError:
            raise ImportError("To use the GCP Secret Manager Resolver you need to: `pip install google-cloud-secret-manager`")
        return secretmanager.SecretManagerServiceClient(credentials=self._credentials)


class GCPSecretManagerResolver(Resolver, GCPSecretManagerMixin):

    def __init__(self, credentials=None, project_id=None, encoding="UTF-8", *args, **kwargs):
        super().__init__(credentials, project_id, *args, **kwargs)
        self.encoding = encoding

    def __call__(self, name: str):
        name_fields = self._parse_secret_name(name)
        secret_name = self._build_secret_name(**name_fields)
        response = self.client.access_secret_version(request={"name": secret_name})
        return response.payload.data.decode(self.encoding)

    def _parse_secret_name(self, name: str) -> Dict[str, str]:
        secret_comps = iter(name.split("/"))
        try:
            secret_dict = {k: v for k, v in zip(secret_comps, secret_comps)}
        except:
            ValueError("Failure parsing secret name.")

        if 'secrets' not in secret_dict.keys():
            raise ValueError("You must provide at least `secrets/<secret_id>`")
        if 'projects' not in secret_dict.keys():
            secret_dict['projects'] = self._project_id
        if 'versions' not in secret_dict.keys():
            secret_dict['versions'] = "latest"

        return secret_dict

    @staticmethod
    def _build_secret_name(projects, secrets, versions):
        return f"projects/{projects}/secrets/{secrets}/versions/{versions}"
