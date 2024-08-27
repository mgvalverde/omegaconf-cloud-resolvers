from .aux import try_cast_to_dict
from .base import AWSMixin
from ..base import Resolver

class AWSSecretManagerMixin(AWSMixin):
    def get_client(self):
        return self._session.client('secretsmanager')


class AWSSecretsManagerResolver(Resolver, AWSSecretManagerMixin):

    def __init__(self, session=None, infere_json=False, *args, **kwargs):
        super().__init__(session, *args, **kwargs)
        self._infere_json = infere_json


    def __call__(self, name):
        secret = self.client.get_secret_value(SecretId=name)

        try:
            secret = secret["SecretString"]
            if self._infere_json:
                return try_cast_to_dict(secret)
            else:
                return secret
        except KeyError:
            return secret["SecretBinary"]
