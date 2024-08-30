from typing import Dict

from omegaconf_cloud_resolvers.resolvers.base import JsonType
from .base import GCPMixin
from ..base import PluginResolver


class GCPSecretManagerMixin(GCPMixin):
    """
    Mixin to handle the auth client generation for GCP Secret Manager
    """

    def get_client(self):
        try:
            from google.cloud import secretmanager
        except ImportError:
            raise ImportError(
                "To use the GCP Secret Manager PluginResolver you need to: `pip install google-cloud-secret-manager`"
            )
        return secretmanager.SecretManagerServiceClient(credentials=self._credentials)


class GCPSecretManagerResolver(PluginResolver, GCPSecretManagerMixin):
    """
    Resolver for the GCP Secret Manager.

    Methods:
        __init__(credentials=None, project_id=None, encoding="UTF-8", *args, **kwargs):
            Initializes the resolver with optional credentials, project ID, and encoding.
            If no credentials or project_id are provided, they'll be infered from the default credentials,
            if condigured.

        __call__(name):
            Resolves the secret by its name and returns the decoded secret data.

    Example:
        Example 1:
        ```python
        >>> resolver = GCPSecretManagerResolver(credentials=my_credentials, project_id="my_project")
        >>> secret_data = resolver("projects/my_project/secrets/my_secret/versions/latest")
        >>> print(secret_data)
        ```

        Example 2: retrieve the latest version of your secret while infering the project
        ```python
        >>> resolver = GCPSecretManagerResolver()
        >>> secret_data = resolver("my_secret")
        >>> print(secret_data)
        ```

        Example 3: retrieve a given version of your secret while infering the project
        ```python
        >>> resolver = GCPSecretManagerResolver()
        >>> secret_data = resolver("secrets/my_secret/versions/1")
        >>> print(secret_data)
        ```
    """

    def __init__(
            self, credentials=None, project_id: str = None, encoding: str = "UTF-8", *args, **kwargs
    ):
        """
        Initializes the GCPSecretManagerResolver.

        Args:
            credentials (google.auth.credentials.Crendential): The google.auth.credentials.Crendential to
                access GCP Secret Manager. If none provided, and uses the default project configured locally.
            project_id: The GCP project ID. If none provided, tries to use the default project configured locally.
            encoding: The encoding used to decode the secret data.
        """
        super().__init__(credentials, project_id, *args, **kwargs)
        self.encoding = encoding

    def __call__(self, name: str) -> JsonType:
        """
        Resolves the secret by its name and returns the decoded secret data.

        Args:
            name (str): The name of the secret to resolve.
                Names must follow the following syntax: `<secret_name>`, `secrets/<secret_name>`,
                `secrets/<secret_name>/versions/<version>`,
                 `projects/<project-id>/secrets/<secret_name>/versions/<version>`

        Returns:
            (str): The decoded secret data.

        Raises:
            ValueError: If the secret name cannot be parsed or if required components are missing.

        """
        name_fields = self._parse_secret_name(name)
        secret_name = self._build_secret_name(**name_fields)
        response = self.client.access_secret_version(request={"name": secret_name})
        return response.payload.data.decode(self.encoding)

    def _parse_secret_name(self, name: str) -> Dict[str, str]:
        """
        Parses the secret name and returns a dictionary with the necessary components.

        Args:
            name (str): The name of the secret to parse.

        Returns:
            Dict[str, str]: A dictionary containing the components of the secret name.

        Raises:
            ValueError: If the secret name cannot be parsed or if required components are missing.
        """
        if "/" in name:
            # Handle cases like projects/projectA/secrets/secretID, secrets/secretID
            secret_comps = iter(name.split("/"))
            try:
                secret_dict = {k: v for k, v in zip(secret_comps, secret_comps)}
            except Exception:
                ValueError("Failure parsing secret name.")
        else:
            # Handles if just 'secretID' is provided
            secret_dict = {"secrets": name}

        if "secrets" not in secret_dict.keys():
            raise ValueError("You must provide at least `secrets/<secret_id>`")
        if "projects" not in secret_dict.keys():
            secret_dict["projects"] = self._project_id
        if "versions" not in secret_dict.keys():
            secret_dict["versions"] = "latest"

        return secret_dict

    @staticmethod
    def _build_secret_name(projects: str, secrets: str, versions: str) -> str:
        """
        Constructs the full secret name from its components.

        Args:
            projects (str): The GCP project ID.
            secrets (str): The secret ID.
            versions (str): The version of the secret.

        Returns:
            str: The full secret name in the format 'projects/{projects}/secrets/{secrets}/versions/{versions}'.
        """
        return f"projects/{projects}/secrets/{secrets}/versions/{versions}"
