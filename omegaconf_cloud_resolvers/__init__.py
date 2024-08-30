import logging
from typing import Callable, Dict, Any

from omegaconf import OmegaConf

from .resolvers.base import JsonType

logger = logging.getLogger("omegaconf.plugin.cloud")


def register_custom_resolvers(*args: Callable[..., JsonType], **kwargs: Dict[str, Callable[..., JsonType]]):
    """
    Registers multiple custom resolvers at once for OmegaConf.

    This function allows you to register multiple custom resolvers either by passing them as positional arguments
    or as keyword arguments. If only a callable is provided, the name used to register the callable will be its
    function name. If there are any name collisions between the positional and keyword arguments, a ValueError
    will be raised.

    Args:
        *args: Variable length list of callables to register as resolvers.
        **kwargs: Arbitrary keyword arguments where the key is the name of the resolver and the value is the callable.

    Raises:
        ValueError: If there are any name collisions between the positional and keyword arguments.

    Example:
        ```python
        def custom_resolver1():
            return "value1"
        def custom_resolver2():
            return "value2"
        register_custom_resolvers(custom_resolver1, custom_resolver2=my_custom_resolver2)
        ```
    """

    def _get_callable_name(func: Callable):
        return func.__name__

    def _get_collision_keys(dict1: Dict[str, Any], dict2: Dict[str, Any]):
        # Convert the dictionary keys to sets
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())
        shared_keys = keys1.intersection(keys2)
        return shared_keys

    args_expand = {_get_callable_name(x): x for x in args}
    resolvers = {**args_expand, **kwargs}
    collision_keys = _get_collision_keys(args_expand, kwargs)
    if collision_keys:
        raise ValueError(
            f"Collision name on resolvers: {collision_keys}, provide key-word for those function with the same name"
        )
    i = 0  # needed in case of no injection
    for i, (name, func) in enumerate(resolvers.items(), 1):
        name = name or _get_callable_name(func)
        OmegaConf.register_new_resolver(name, func)
    logger.info("Custom resolvers registered: %s", i)


__all__ = [
    "register_custom_resolvers",
]
