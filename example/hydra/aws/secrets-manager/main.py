# Import necessary libraries
import hydra
from omegaconf import DictConfig

from omegaconf_cloud_resolvers import register_custom_resolvers
from omegaconf_cloud_resolvers.resolvers.aws import AWSSecretsManagerResolver

resolvers = {
    "aws_secretsmanager": AWSSecretsManagerResolver(),
    "aws_secretsmanager_parsed": AWSSecretsManagerResolver(infer_json=True),
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
