import pytest
from omegaconf import OmegaConf

from omegaconf_cloud_resolvers import register_custom_resolvers


def test_inject_resolver():
    def sample_resolver(x):
        return x * 2

    register_custom_resolvers(double=sample_resolver)
    assert OmegaConf.create({"value": "${double:2}"})["value"] == 4
    OmegaConf.clear_resolvers()


def test_inject_resolvers():
    def resolver1(x, y):
        return x + y

    def resolver2(x):
        return x * 2

    register_custom_resolvers(resolver1, resolver2)
    assert OmegaConf.create(
        {"value1": "${resolver1:2,1}", "value2": "${resolver2:2}"}
    ) == {"value1": 3, "value2": 4}
    OmegaConf.clear_resolvers()


def test_inject_resolvers_with_collision():
    def resolver1(x):
        return x + 1

    with pytest.raises(ValueError, match="Collision name on resolvers"):
        register_custom_resolvers(resolver1, resolver1=lambda x: x + 1)
    OmegaConf.clear_resolvers()
