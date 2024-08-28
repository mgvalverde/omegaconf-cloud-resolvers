from .aux import try_cast_to_dict
from .base import AWSMixin
from ..base import PluginResolver


class AWSSecretManagerMixin(AWSMixin):
    def get_client(self):
        return self._session.client("secretsmanager")


class AWSSecretsManagerResolver(PluginResolver, AWSSecretManagerMixin):
    def __init__(self, session=None, infer_json=False, *args, **kwargs):
        super().__init__(session, *args, **kwargs)
        self._infer_json = infer_json

    def __call__(self, name):
        secret = self.client.get_secret_value(SecretId=name)

        try:
            secret = secret["SecretString"]
            if self._infer_json:
                return try_cast_to_dict(secret)
            else:
                return secret
        except KeyError:
            return secret["SecretBinary"]
