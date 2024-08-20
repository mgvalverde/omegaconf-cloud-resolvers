from .base import AWSSecretsManagerRetriever, AWSParameterStoreRetriever

try:
    import boto3
except ImportError:
    raise ImportError("To use the AWS resolver, you need to install boto3: `pip install boto3`")

__all__ = [
    "AWSSecretsManagerRetriever",
    "AWSParameterStoreRetriever"
]
