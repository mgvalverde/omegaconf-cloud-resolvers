from typing import List

from omegaconf_cloud_resolvers.injector import CustomResolverInjector


# NOTE: defining  Literal["aws", ...] gets type warning: Expected type 'Literal["aws", ...]', got 'str' instead,
#  https://youtrack.jetbrains.com/issue/PY-46450/Expected-Literal-got-str-when-str-is-stored-in-a-variable
def init_cloud_resolvers(*args):
    from omegaconf_cloud_resolvers.resolvers.aws import (
        AWSSecretsManagerResolver,
        AWSParameterStoreResolver,
    )
    from omegaconf_cloud_resolvers.resolvers import GCPSecretManagerResolver

    CLOUD_PROVIDERS = ["aws", "gcp"]
    RESOLVERS = {
        "aws_secretsmanager": AWSSecretsManagerResolver,
        "aws_parameterstore": AWSParameterStoreResolver,
        "gcp_secretmanager": GCPSecretManagerResolver,
    }

    if set(args) - set(CLOUD_PROVIDERS):
        _ = ", ".join(CLOUD_PROVIDERS)
        raise ValueError(f"The only possible providers currently are: {_} ")

    def match_prefix(prefixes: List[str], value: str):
        for prefix in prefixes:
            if value.startswith(prefix):
                return True
        return False

    resolvers_chosen = {k: v() for k, v in RESOLVERS.items() if match_prefix(args, k)}

    CustomResolverInjector.inject_resolvers(**resolvers_chosen)


__all__ = [
    "CustomResolverInjector",
    "init_cloud_resolvers",
]
