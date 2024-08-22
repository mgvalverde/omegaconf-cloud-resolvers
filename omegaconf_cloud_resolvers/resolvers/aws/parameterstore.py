from .base import AWSMixin
from ..base import Resolver
from .aux import try_cast_to_number

class AWSParameterStoreMixin(AWSMixin):
    def get_client(self):
        return self._session.client('ssm')

class AWSParameterStoreResolver(Resolver, AWSParameterStoreMixin):
    def __init__(self, session=None, decrypt=True, is_list=True, enforce_numerical=True, *args, **kwargs):
        super().__init__(session, *args, **kwargs)
        self._decrypt = decrypt
        self._is_list = is_list
        self._enforce_numerical = enforce_numerical

    def __call__(self, name):
        value = self.client.get_parameter(Name=name, WithDecryption=self._decrypt)
        ptype = value["Parameter"]["Type"]
        pvalue = value["Parameter"]["Value"]
        return self.parse_value(pvalue, ptype, self._decrypt, self._is_list, self._enforce_numerical)

    @staticmethod
    def parse_value(value, type_, decrypt, is_list, enforce_numerical):
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
