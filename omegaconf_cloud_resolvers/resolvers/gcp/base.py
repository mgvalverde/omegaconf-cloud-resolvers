from abc import ABC

import google.auth

from ..base import ClientMixin


class GCPMixin(ClientMixin, ABC):
    def __init__(self, credentials=None, project_id=None):
        if credentials is None or project_id is None:
            credentials_, project_id_ = google.auth.default()
        else:
            credentials_, project_id_ = None, None
        self._credentials = credentials or credentials_
        self._project_id = project_id or project_id_
        self.client = self.get_client()
