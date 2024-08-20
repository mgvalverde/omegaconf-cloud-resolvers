import google.auth
from google.cloud import secretmanager


def count_occurrences(string, char):
    n = 0
    for c in string:
        if c == char:
            n += 1
    return n


class GCPSecretManagerRetriever:

    def __init__(self, credentials=None, project_id=None, **kwargs):
        if credentials is None or project_id is None:
            credentials_, project_id_ = google.auth.default()
        else:
            credentials_, project_id_ = None, None

        self._credentials = credentials or credentials_
        self._project_id = project_id or project_id_
        self._config = kwargs
        self._client = secretmanager.SecretManagerServiceClient(credentials=self._credentials)

    def __call__(self, name):
        n = count_occurrences(name, "/")
        if n == 0:
            version = None
            secret_id = name
            project_id = self._project_id
        elif n == 1:
            secret_id, version = name.split("/")
            project_id = self._project_id
        elif n == 2:
            project_id, secret_id, version = name.split("/")
        else:
            raise ValueError(
                "You need to provide: `<secret-id>`, `<secret-id>/<version-id>` or `<project-id>/<secret-id>/<version-id>`.")

        return self.retrieve_secret(secret_id, version, project_id)


    def retrieve_secret(self, secret_id, version_id=None, project_id=None):
        name = self._client.secret_path(project_id, secret_id)
        if version_id:
            name += f"/versions/{version_id}"
        else:
            name += f"/versions/latest"
        response = self._client.access_secret_version(request={"name": name})
        encoding = self._config.get("encoding", "UTF-8")
        return response.payload.data.decode(encoding)

    # name = "/versions/latest"
    # def parse_name(self, name):
    #     ""