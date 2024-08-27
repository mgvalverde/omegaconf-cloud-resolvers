import pytest
from omegaconf import OmegaConf
from omegaconf_cloud_resolvers import (
    CustomResolverInjector,
)  # Replace 'your_module' with the actual module name


def test_inject_resolver():
    def sample_resolver(x):
        return x * 2

    CustomResolverInjector.inject_resolver(sample_resolver, "double")
    assert OmegaConf.create({"value": "${double:2}"})["value"] == 4
    OmegaConf.clear_resolvers()


def test_inject_resolvers():
    def resolver1(x, y):
        return x + y

    def resolver2(x):
        return x * 2

    CustomResolverInjector.inject_resolvers(resolver1, resolver2)
    assert OmegaConf.create(
        {"value1": "${resolver1:2,1}", "value2": "${resolver2:2}"}
    ) == {"value1": 3, "value2": 4}
    OmegaConf.clear_resolvers()


def test_inject_resolvers_with_collision():
    def resolver1(x):
        return x + 1

    with pytest.raises(ValueError, match="Collision name on resolvers"):
        CustomResolverInjector.inject_resolvers(resolver1, resolver1=lambda x: x + 1)
    OmegaConf.clear_resolvers()


def test_get_collision_keys():
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    assert CustomResolverInjector._get_collision_keys(dict1, dict2) == {"b"}
    OmegaConf.clear_resolvers()


def test_get_callable_name():
    def sample_func():
        pass

    assert CustomResolverInjector._get_callable_name(sample_func) == "sample_func"
    OmegaConf.clear_resolvers()
