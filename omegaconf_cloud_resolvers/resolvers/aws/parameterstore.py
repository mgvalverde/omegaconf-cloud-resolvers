from .base import AWSMixin
from ..base import Resolver
from .aux import try_cast_to_number

class AWSParameterStoreMixin(AWSMixin):
    def get_client(self):
        return self._session.client('ssm')

class AWSParameterStoreResolver(Resolver, AWSParameterStoreMixin):
    def __init__(self, session=None, decrypt=True, infere_types=False, *args, **kwargs):
        super().__init__(session, *args, **kwargs)
        self._decrypt = decrypt
        self._infere_types = infere_types

    def __call__(self, name):
        value = self.client.get_parameter(Name=name, WithDecryption=self._decrypt)
        ptype = value["Parameter"]["Type"]
        pvalue = value["Parameter"]["Value"]
        return self.parse_value(pvalue, ptype, self._decrypt, self._infere_types)

    @staticmethod
    def parse_value(value, type_, decrypt, infere_types):
        if (type_ == 'StringList') and not decrypt:
            values = value.split(",")
            if infere_types:
                return [try_cast_to_number(v) for v in values]
            else:
                return values
        else:
            if infere_types:
                return try_cast_to_number(value)
            else:
                return value
