from functools import lru_cache
from functools import partial
from typing import Dict

from .base import AzureMixin
from ..base import PluginResolver


@lru_cache
def get_az_client_helper(credential, keyvault):
    try:
        from azure.keyvault.secrets import SecretClient
    except ImportError:
        raise ImportError(
            "To use the Microsoft Azure resolvers, you need to: `pip install omegaconf_cloud_resolvers[az]`"
        )
    KVUri = f"https://{keyvault}.vault.azure.net"
    return SecretClient(vault_url=KVUri, credential=credential)


class AzureKeyVaulMixin(AzureMixin):
    """
    Mixin to handle the auth client generation for Microsoft Azure Key Vault
    """

    def get_client(self):
        def _get_az_client(credentials, keyvault, secret, version=None):
            return get_az_client_helper(credentials, keyvault).get_secret(
                secret, version
            )

        return partial(_get_az_client, credentials=self._credentials)


# TODO: refactor name parser to allow: name="<keyvault_id>/<secret_name>/<version>"
# NOTE: currently: name="keyvault/<keyvault_id>/secret/<secret_name>/version/<version>"


class AzureKeyVaultResolver(PluginResolver, AzureKeyVaulMixin):
    """
    Resolver for the Azure Key Vault.

    Methods:
        __init__(credential=None, *args, **kwargs):
            Initializes the resolver with optional credentials.
            If no credential is provided, they'll be infered from the default credentials,
            if condigured.

        __call__(name):
            Resolves the secret by its name and returns the decoded secret data.

    Example:
        Example 1: retrieve a given version of your secret
        ```python
        >>> from azure.identity import DefaultAzureCredential
        >>> my_credentials = DefaultAzureCredential()
        >>> resolver = AzureKeyVaultResolver(credentials=my_credentials)
        >>> secret_data = resolver("keyvault/MyKeyVault123/secret/SecretName/version/339d8635b22344b2b6117588ef94a22q")
        >>> print(secret_data)
        ```

        Example 2: retrieve the latest version of your secret
        ```python
        >>> resolver = AzureKeyVaultResolver()
        >>> secret_data = resolver("keyvault/MyKeyVault123/secret/SecretName")
        >>> print(secret_data)
        ```
    """

    def __call__(self, name: str) -> str:
        """
        Resolves the secret by its name and returns the decoded secret data.

        Args:
            name (str): The name of the secret to resolve.
                Names must follow the following syntax:
                `keyvault/<keyvault_id>/secret/<secret_name>`,
                 `keyvault/<keyvault_id>/secret/<secret_name>/version/<version>`

        Returns:
            (str): The secret data.

        Raises:
            ValueError: If the secret name cannot be parsed or if required components are missing.

        """
        name_fields = self._parse_secret_name(name)
        response = self.client(
            keyvault=name_fields["keyvault"],
            secret=name_fields["secret"],
            version=name_fields["version"],
        )
        return response.value

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
        secret_dict = {}
        if "/" not in name:
            raise ValueError(
                "You must provide at least `keyvault/<keyvault_id>/secret/<secret_id>`"
            )

        secret_comps = iter(name.split("/"))
        try:
            secret_dict = {k: v for k, v in zip(secret_comps, secret_comps)}
        except Exception:
            ValueError("Failure parsing secret name.")

        if not {"secret", "keyvault"}.issubset(secret_dict.keys()):
            raise ValueError(
                "You must provide at least `keyvault/<keyvault_id>/secret/<secret_id>`"
            )
        if "version" not in secret_dict.keys():
            secret_dict["version"] = None
        return secret_dict
