from .parameterstore import AWSParameterStoreResolver
from .secretsmanager import AWSSecretsManagerResolver

__all__ = ["AWSSecretsManagerResolver", "AWSParameterStoreResolver"]
