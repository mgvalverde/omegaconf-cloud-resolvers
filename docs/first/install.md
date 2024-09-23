# Installation

You can install the package only with the required dependencies for your environment.

Using `pip`:

* For AWS:

```bash
pip install omegaconf-cloud-resolvers[aws]
```

* For GCP

```bash
pip install omegaconf-cloud-resolvers[gcp]
```

* For Azure

```bash
pip install omegaconf-cloud-resolvers[az]
```

# Hydra

If you make use of `hydra` to load your configuration as well, it needs to be installed separately:

```bash
pip install hydra-core
```
