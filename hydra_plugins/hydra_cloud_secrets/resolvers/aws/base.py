import boto3
from ..base import ConfRetriever
from .aux import try_cast_to_number

class AWSConfRetriever(ConfRetriever):
    def __init__(self, session: boto3.Session = None, *args, **kwargs):
        self._session = session or boto3.Session()
        self._set_config(*args, **kwargs)

    def _set_config(self, *args, **kwargs):
        pass


class AWSSecretsManagerRetriever:

    def __init__(self, session: boto3.Session = None, *args, **kwargs):
        self._session = session or boto3.Session()
        self.client =  self._session.client('secretsmanager')

    def __call__(self, name):
        secret = self.client.get_secret_value(SecretId=name)

        try:
            return secret["SecretString"]
        except KeyError:
            return secret["SecretBinary"]


class AWSParameterStoreRetriever:

    def __init__(self, session: boto3.Session = None, decrypt=True, is_list=True, enforce_numerical=True):
        self._session = session or boto3.Session()
        self.client = self._session.client('ssm')
        self._decrypt = decrypt
        self._is_list = is_list
        self._enforce_numerical = enforce_numerical

    def __call__(self, name):
        value = self.client.get_parameter(Name=name, WithDecryption=self._decrypt)
        ptype = value["Parameter"]["Type"]
        pvalue = value["Parameter"]["Value"]
        return self.parse_parameter(pvalue, ptype, self._decrypt, self._is_list, self._enforce_numerical)

    @staticmethod
    def parse_parameter(value, type_, decrypt, is_list, enforce_numerical):
        if (type_ == 'StringList') and is_list and not decrypt:
            values = value.split(",")
            if enforce_numerical:
                return [try_cast_to_number(v) for v in values]
            else:
                return values
        else:
            if enforce_numerical:
                return try_cast_to_number(value)
            else:
                return value
