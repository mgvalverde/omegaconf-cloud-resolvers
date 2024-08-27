from typing import Callable, Dict, Any
import logging
from omegaconf import OmegaConf

logger = logging.getLogger(__name__)


class CustomResolverInjector:
    """

    """

    @classmethod
    def inject_resolver(cls, func: Callable, name: str = None):
        name = name or cls._get_callable_name(func)
        OmegaConf.register_new_resolver(name, func)

    @classmethod
    def inject_resolvers(cls, *args, **kwargs):
        args_expand = {cls._get_callable_name(x): x for x in args}
        resolvers = {**args_expand, **kwargs}
        collision_keys = cls._get_collision_keys(args_expand, kwargs)
        if collision_keys:
            raise ValueError(f"Collision name on resolvers: {collision_keys}, provide key-word for those function with the same name")
        i = 0  # needed in case of no injection
        for i, (name, func) in enumerate(resolvers.items(), 1):
            cls.inject_resolver(func, name)
        logger.info(f"Injected {i} custom resolvers")

    @staticmethod
    def _get_collision_keys(dict1: Dict[str, Any], dict2: Dict[str, Any]):
        # Convert the dictionary keys to sets
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())
        # Find the intersection of both sets of keys
        shared_keys = keys1.intersection(keys2)
        return shared_keys

    @staticmethod
    def _get_callable_name(func: Callable):
        return func.__name__
