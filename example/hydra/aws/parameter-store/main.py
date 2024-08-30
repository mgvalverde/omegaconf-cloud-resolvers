# Import necessary libraries
import hydra
from omegaconf import DictConfig
import logging
from omegaconf_cloud_resolvers import register_custom_resolvers
from omegaconf_cloud_resolvers.resolvers.aws import AWSParameterStoreResolver

logger = logging.getLogger(__name__)

resolvers = {
    "get_aws_param": AWSParameterStoreResolver(infer_types=False, decrypt=False),
    "get_aws_decrypt": AWSParameterStoreResolver(infer_types=True, decrypt=True),
    "get_aws_param_list": AWSParameterStoreResolver(infer_types=True, decrypt=False),
    "get_aws_param_list_str": AWSParameterStoreResolver(infer_types=False, decrypt=False),
}

register_custom_resolvers(**resolvers)

config_fname = "config"
config_dir = ""


# Main function
@hydra.main(version_base=None, config_path=config_dir, config_name=config_fname)
def main(cfg: DictConfig):
    for k, v in cfg.items():
        print(k, ":", type(v), "=>", v, end="\n\n")


if __name__ == "__main__":
    main()
