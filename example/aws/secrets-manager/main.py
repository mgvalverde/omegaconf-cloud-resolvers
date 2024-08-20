# Import necessary libraries
import hydra
from omegaconf import DictConfig

from hydra_plugins.hydra_cloud_secrets import HydraResolverInjector
from hydra_plugins.hydra_cloud_secrets.resolvers.aws import AWSSecretsManagerRetriever

resolvers = {
    "get_secret": AWSSecretsManagerRetriever(),
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
