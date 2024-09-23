# Integration with Hydra

If you are new to Hydra, you might want to have a look at the [docs](https://hydra.cc/docs/intro/).
Hydra is a powerful framework for configuring complex applications.
It allows you to compose configurations dynamically and provides a flexible way to manage them
To use Hydra, ensure that it is installed in your environment. If it is not installed, you can do so
by running the following command:

```bash
pip install -U hydra-core
```

In this example, we will demonstrate how to use Hydra in conjunction with the AWS environment and the
[AWS SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html).

## Set-up the Permissions

### Credentials and Permissions

If you are running this example from your local machine, ensure that you have configured your AWS credentials.

You might need to install the [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
if you don't have it yet.

To verify that you have the necessary permissions to access the AWS SSM Parameter Store
and to create and retrieve parameters, review
the [policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-access.html)
attached to your user's role. Ensure that your IAM user or role has the appropriate permissions.

### Configuring AWS CLI

After installing the AWS CLI, configure it with your credentials by running:

```bash
aws configure
```
You will be prompted to enter your AWS Access Key ID, Secret Access Key, region, and output format.
This configuration is stored in the `~/.aws/credentials` and `~/.aws/config` files.

## Example

### Create a secret parameter.

To create a secret parameter using the AWS CLI, run the following command:

```bash
aws ssm put-parameter --name "/projectBlue/envA/secret" --value "MySecureParameterValue" --type "SecureString"
```

Make sure to keep the parameter's name handy, as we will use it later in our configuration file.


### Write your script

Create a `main.py` file with the following content:

```python
import hydra
from omegaconf import DictConfig
import boto3
from omegaconf_cloud_resolvers import register_custom_resolvers
from omegaconf_cloud_resolvers.resolvers.aws import AWSParameterStoreResolver

session = boto3.Session(...)  # Replace ... with you actual auth info, e.g: profile_name

resolvers = {
    "get_aws_secret": AWSParameterStoreResolver(session=session),
}

register_custom_resolvers(**resolvers)

config_fname = "config"
config_dir = "."


@hydra.main(version_base=None, config_path=config_dir, config_name=config_fname)
def main(cfg: DictConfig):
    print(cfg["secret"])


if __name__ == "__main__":
    main()
```

Let's understand each line step by step.

1. **Define the resolver to retrieve the secret.**
   Each key in the `resolvers` dictionary will be the name of the function that you can use in your configuration files.
   The dictionary's value must be a callable, which in this case, it is, since all the cloud resolvers are
   provided with a `__call__` method.


```python
resolvers = {
    "get_aws_secret": AWSSecretsManagerResolver(session=session),
}
```

2. **Register the resolvers using the function `register_custom_resolvers`**.
   This step is what will ensure that you can access your secret using the resolvers.

```python
register_custom_resolvers(**resolvers)
```

3. **Provide the reference to where our config file will be (`.`) and the name without extension (`config`).**

```python

config_fname = "config"
config_dir = "."
```

4. **Use the Hydra decorator on your main function.**
   Within the main function scope, you'll have access to the configuration values stored in `cfg`.

```python
@hydra.main(version_base=None, config_path=config_dir, config_name=config_fname)
def main(cfg: DictConfig):
    print(cfg["secret"])

```

!!! note "Alternative without decorator"

    In case that you don't want to use the decorator `@hydra.main`
    and a main function, you can alternatively use.
    ```python
    from hydra.utils import instantiate
    from hydra import compose, initialize

    ... # your other code

    initialize(config_path=".")
    cfg_raw = compose(config_name="config")  # Load and merge
    cfg = instantiate(cfg_raw)               # Interpolate values
    ```

# Configuration file

On the same level as the `main.py`, create a `config.yaml`.

```yaml
param1: 1
param2: "value"
secret: "${get_aws_secret:/projectBlue/envA/secret}"
```

## Run the script

If you run your script, you should be able to see your secret printed.

```python
python main.py
```

By following these steps, you can integrate Hydra into your Python projects and leverage AWS services effectively
to retrieve your secrets and parameters securely.
