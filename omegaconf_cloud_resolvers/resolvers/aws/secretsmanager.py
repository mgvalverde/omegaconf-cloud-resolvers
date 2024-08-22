from .base import AWSMixin
from ..base import Resolver

class AWSSecretManagerMixin(AWSMixin):
    def get_client(self):
        return self._session.client('secretsmanager')


class AWSSecretsManagerResolver(Resolver, AWSSecretManagerMixin):

    def __call__(self, name):
        secret = self.client.get_secret_value(SecretId=name)

        try:
            return secret["SecretString"]
        except KeyError:
            return secret["SecretBinary"]
