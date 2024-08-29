from typing import Literal

from example.others.exp.exp import recursive
from .aux import try_infer_and_cast
from .base import AWSMixin
from ..base import PluginResolver
from ... import logger


class AWSParameterStoreMixin(AWSMixin):
    def get_client(self):
        return self._session.client("ssm")


AWS_PARAMETER_TYPE = Literal["String", "StringList", "SecureString"]


class AWSParameterStoreResolver(PluginResolver, AWSParameterStoreMixin):
    """
    Resolver for AWS Systems Manager Parameter Store

    Example:
        Example 1: Retrieve a secret as a string
        ```python
        >>> resolver = AWSParameterStoreResolver(session=boto3_session,decrypt=True,infer_types=True)
        >>> parameter_value = resolver('my/parameter/name') # Contains 1 value
        >>> print(parameter_value)  # 'my_secret_value
        ```
        Example 2: Retrieve a StringList
        ```python
        >>> resolver = AWSParameterStoreResolver(session=boto3_session,decrypt=True,infer_types=True)
        >>> parameter_value = resolver('my/parameter/list/name') # Contains 1 value
        >>> print(parameter_value)  # ['my_secret_value', 'my_secret_value_2']
        ```
    """

    def __init__(self, session=None, decrypt=True, infer_types=False, *args, **kwargs):
        """
        Initializes the AWSParameterStoreResolver.

        Args:
            session (boto3.Session, optional): An optional boto3 session to use for AWS interactions.
            decrypt (bool, optional): If True, decrypts the parameter value. Defaults to True.
            infer_types (bool, optional): If True, attempts to infer the type of the parameter value, it might be
              more useful when the parameter is of type StringList if mixed types are found. Defaults to False.
            *args: Extra argument list passed to the Mixin init.
            **kwargs: Extra arbitrary keyword arguments passed to the Mixin init.
        """
        super().__init__(session, *args, **kwargs)
        self._decrypt = decrypt
        self._infer_types = infer_types

    def __call__(self, name):
        """
        Retrieves a parameter from AWS Systems Manager Parameter Store.

        Args:
            name (str): The name of the parameter to retrieve.
             Retrieve a single parameter,

        Returns:
            str or list or int or float: The parameter value. If the parameter is a StringList and _decrypt is False,
                                         it returns a list of strings or numbers (if _infer_types is True).
                                         Otherwise, it returns the parameter value as a string, int, or float
                                         depending on the type inference.
        """
        if name.endswith("/*") or name.endswith("/**"):
            if name.endswith("/**"):    # If '**' access recursively, if only '*' just to the first level.
                recursive = True
                name = name.removesuffix("/**")
            else:
                recursive = False
                name = name.removesuffix("/*")
            return  self._get_path_parameters(name, recursive)
        else:
            return self._get_single_parameter(name)

    def _get_single_parameter(self, name):
        value = self.client.get_parameter(Name=name, WithDecryption=self._decrypt)
        ptype = value["Parameter"]["Type"]
        pvalue = value["Parameter"]["Value"]
        return self._parse_value(pvalue, ptype, self._decrypt, self._infer_types)

    def _get_path_parameters(self, name, recursive):
        rparameters = []
        # Use the get_parameters_by_path method to retrieve parameters
        response = self.client.get_parameters_by_path(
            Path=name,
            Recursive=recursive,
            WithDecryption=self._decrypt
        )
        rparameters.extend(response['Parameters'])

        # Check if there are more parameters to retrieve
        while 'NextToken' in response:
            response = self._decrypt.get_parameters_by_path(
                Path=name,
                Recursive=recursive,
                WithDecryption=self._decrypt,
                NextToken=response['NextToken']
            )
            rparameters.extend(response['Parameters'])

        parameters = {}
        for parameter in rparameters:
            pname, ptype, pvalue = parameter["Name"], parameter["Type"], parameter["Value"]
            pname = pname.replace(name, "").lstrip("/")
            parameters[pname] = self._parse_value(
                value=pvalue,
                type_=ptype,
                decrypt=self._decrypt,
                infer_types=self._infer_types
            )
        return parameters

    @staticmethod
    def _parse_value(value: str, type_: AWS_PARAMETER_TYPE, decrypt: bool = False, infer_types: bool = False):
        """
        Parses the parameter value based on its type and the provided flags.

        Args:
            value (str): The parameter value to parse.
            type_ (Literal["String", "StringList", "SecureString"]): The type of the parameter.
            decrypt (bool): A flag indicating whether the parameter value should be decrypted, for "String", "StringList",
              it does make any difference. For "SecureString", if False, it returns the encrypted string.
            infer_types (bool): A flag indicating whether to attempt to infer and cast the type of the parameter value.
              Note: it does not strip strings, so "a,b, c" will return ["a", "b", " c"]

        Returns:
            str or list or int or float: The parsed parameter value. If the parameter is a StringList and decrypt is False,
                                         it returns a list of strings or numbers (if infer_types is True).
                                         Otherwise, it returns the parameter value as a string, int, or float
                                         depending on the type inference.
        """

        if type_ == "StringList":
            values = value.split(",")
            if infer_types:
                return [try_infer_and_cast(v) for v in values]
            else:
                return values

        if type_ == "SecureString" and not decrypt:
            if infer_types:
                logger.warning("infer_types is ignored when parameter type is 'SecureString' and decrypt is False")
            return value  # returns the encrypted value

        if infer_types:
            return try_infer_and_cast(value)
        else:
            return value
