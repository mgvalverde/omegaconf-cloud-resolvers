from importlib.util import find_spec

if not find_spec("boto3"):
    raise ImportError(
        "To use the AWS resolvers, you need to: `pip install omegaconf_cloud_resolvers[aws]`"
    )

from .parameterstore import AWSParameterStoreResolver
from .secretsmanager import AWSSecretsManagerResolver

__all__ = ["AWSSecretsManagerResolver", "AWSParameterStoreResolver"]
