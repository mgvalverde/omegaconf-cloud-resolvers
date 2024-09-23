from importlib.util import find_spec

if not find_spec("azure.keyvault.secrets") or not find_spec("azure.identity"):
    raise ImportError(
        "To use the Microsoft Azure resolvers, you need to: `pip install omegaconf_cloud_resolvers[az]`"
    )

from .keyvault import AzureKeyVaultResolver

__all__ = [
    "AzureKeyVaultResolver",
]
