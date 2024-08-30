from importlib.util import find_spec

if not find_spec("google.auth"):
    raise ImportError(
        "To use the GCP resolvers, you need to: `pip install omegaconf_cloud_resolvers[gcp]`"
    )

from .secretmanager import GCPSecretManagerResolver

__all__ = [
    "GCPSecretManagerResolver",
]
