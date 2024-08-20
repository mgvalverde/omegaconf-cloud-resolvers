# Import necessary libraries
from pathlib import Path
from functools import partial
import hydra
from omegaconf import DictConfig
import logging
from hydra_plugins.hydra_cloud_secrets import HydraResolverInjector
from hydra_plugins.hydra_cloud_secrets.resolvers.aws import AWSParameterStoreRetriever

logger = logging.getLogger(__name__)

resolvers = {
    "get_aws_param": AWSParameterStoreRetriever(),
    "get_aws_decrypt": AWSParameterStoreRetriever(is_list=True, decrypt=True),
    "get_aws_param_list": AWSParameterStoreRetriever(is_list=True, decrypt=False),
}

hydra_injector = HydraResolverInjector.inject_resolvers(**resolvers)

config_fname = "config"
config_dir = "."

# Main function
@hydra.main(version_base=None, config_path=config_dir, config_name=config_fname)
def main(cfg: DictConfig):
    for k, v in cfg.items():
        print(k, "=>", v, end="\n\n")


if __name__ == '__main__':
    main()
