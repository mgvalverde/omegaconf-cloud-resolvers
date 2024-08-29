from .aux import try_cast_to_dict
from .base import AWSMixin
from ..base import PluginResolver
from ... import logger


class AWSSecretManagerMixin(AWSMixin):
    def get_client(self):
        return self._session.client("secretsmanager")


class AWSSecretsManagerResolver(PluginResolver, AWSSecretManagerMixin):
    """
    Resolver for the AWS Secrets Manager

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

    def __init__(self, session=None, infer_json=False, return_binary=False, *args, **kwargs):
        """
       Initializes the AWSSecretsManagerResolver.

       Args:
           session (boto3.Session, optional): boto3 session to use for AWS interactions. Defaults to None, and uses the default configuration.
           infer_json (bool, optional): If True, attempts to parse the secret as JSON during the __call__. Defaults to False.
           *args: Variable length argument list.
           **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(session, *args, **kwargs)
        self._infer_json = infer_json
        self._return_binary = return_binary
        if self._return_binary and self._infer_json:
            logger.warning("infer_json is only tried for string secrets")

    def __call__(self, name):
        """
        Retrieves a secret from AWS Secrets Manager.
        It prioritizes 'SecretString' over 'SecretBinary'

        Args:
            name (str): The name of the secret to retrieve.

        Returns:
            str or dict: The secret value. If _infer_json is True and the secret is a valid JSON string,
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
            logger.exception("The found secrets does not contain '%s'", e.args[0])
            raise

