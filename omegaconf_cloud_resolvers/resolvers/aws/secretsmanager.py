import logging

from omegaconf_cloud_resolvers.resolvers.aux import try_cast_to_dict
from omegaconf_cloud_resolvers.resolvers.base import JsonType
from .base import AWSMixin
from ..base import PluginResolver

logger = logging.getLogger("omegaconf.plugin.cloud")


class AWSSecretManagerMixin(AWSMixin):
    def get_client(self):
        return self._session.client("secretsmanager")


class AWSSecretsManagerResolver(PluginResolver, AWSSecretManagerMixin):
    """
    Resolver for the AWS Secrets Manager

    Methods:
        __init__(session=None, infer_json=False, return_binary=False, *args, **kwargs):
            Initializes the resolver with a boto3 Session.
            If no Session is provided, it'll be infered from the default credentials,
            if configured.

        __call__(name):
            Resolves the secret by its name and returns the decoded secret data.

    Example:
        Example 1: Retrieve a secret as a string
        ```python
        >>> resolver = AWSSecretsManagerResolver(session=boto3_session, infer_json=True)
        >>> secret_value = resolver('my_secret')
        >>> print(secret_value) # {"a": 1}
        ```

        Example 2: Retrieve a secret and parse it as JSON
        ```python
        >>> resolver = AWSSecretsManagerResolver(session=boto3_session, infer_json=False)
        >>> secret_value = resolver('my_secret')
        >>> print(secret_value) # '{"a": 1}'
        ```


    """

    def __init__(self, session=None, infer_json: bool = False, return_binary: bool = False, *args, **kwargs):
        """
       Initializes the AWSSecretsManagerResolver.

       Args:
           session (boto3.Session): boto3.Session to use for AWS interactions. If none provided, tries to use the default configuration.
           infer_json: If True, tries to parse the secret as JSON during the __call__.
           return_binary: If True, tries to return the binary value from the key `SecretBinary` instead of `SecretString`.
        """
        super().__init__(session, *args, **kwargs)
        self._infer_json = infer_json
        self._return_binary = return_binary
        if self._return_binary and self._infer_json:
            logger.warning("infer_json is only tried for string secrets")

    def __call__(self, name: str) -> JsonType:
        """
        Retrieves a secret from AWS Secrets Manager.
        The default behaviour prioritizes 'SecretString' over 'SecretBinary'

        Args:
            name: The name of the secret to retrieve.

        Returns:
            The secret value. If infer_json is True and the secret is a valid JSON string,
                         it returns a dictionary. Otherwise, it returns the secret as a string.

        Raises:
            KeyError: If the secret does not contain either of "SecretString", "SecretBinary" key.
        """

        secret = self.client.get_secret_value(SecretId=name)

        try:
            if self._return_binary:
                return secret["SecretBinary"]
            else:
                secret = secret["SecretString"]
                if self._infer_json:
                    return try_cast_to_dict(secret)
                else:
                    return secret
        except KeyError as e:
            logger.exception("The found secret does not contain '%s'", e.args[0])
            raise
