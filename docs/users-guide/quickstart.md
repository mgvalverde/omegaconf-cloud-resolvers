# Quickstart

## Introduction to OmegaConf

For those unfamiliar with OmegaConf, it is highly recommended to first review its official
[documentation](https://omegaconf.readthedocs.io/).
In brief, OmegaConf is a YAML-based configuration system that supports merging configurations from multiple sources.


One of OmegaConf's most compelling features is its ability to interpolate values within configuration files.
This is achieved through the use of [Resolvers](https://omegaconf.readthedocs.io/en/2.3_branch/custom_resolvers.html#).
The syntax for interpolation is: `"${<resolver-name>:<args>}"`.

Resolvers can be any type of function. Below is an example demonstrating how to register and use a custom resolver:

```python
from omegaconf import OmegaConf

OmegaConf.register_new_resolver("upper", lambda x: x.upper())

conf = OmegaConf.create({
    "greet": "hello",
    "who": "${upper:world}"
})
print(conf["who"])  # 'WORLD'
```

Alternatively use `register_custom_resolvers`, which allows you to register
many resolvers at once.
They key of the dictionary is the name of the resolver which you need to use
to interpolate.

```python
from omegaconf import OmegaConf
from omegaconf_cloud_resolvers import register_custom_resolvers

resolvers = {
    "upper": lambda x: x.upper(),
    "add_exc": lambda x: x + "!",
}
register_custom_resolvers(**resolvers)

conf = OmegaConf.create({
    "greet": "hello",
    "who": "${add_exc:${upper:world}}"
})
print(conf["who"])  # 'WORLD!'
```

Continue to [Cloud Resolvers](./resolvers.md) to see what the plugin can do.
