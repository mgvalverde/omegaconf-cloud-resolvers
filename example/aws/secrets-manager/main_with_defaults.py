# Import necessary libraries
import hydra
from omegaconf import DictConfig
from omegaconf_cloud_resolvers import init_cloud_resolvers

init_cloud_resolvers("aws")

config_fname = "config_with_defaults"
config_dir = "."


# Main function
@hydra.main(version_base=None, config_path=config_dir, config_name=config_fname)
def main(cfg: DictConfig):
    for k, v in cfg.items():
        print(k, ":", type(v), "=>", v, end="\n\n")


if __name__ == "__main__":
    main()
