# Omegaconf Plugin: Cloud Secrets

This package is a plugin designed to enhance OmegaConf by providing additional custom resolvers to **securely retrieve
sensitive values** that should not be hard-coded in your configuration files.

Currently, there are resolvers for:

* AWS:
    * Secrets Manager
    * Parameter Store
* Google Cloud Platform (GCP):
    * Secret Manager

## Installation

 * AWS: 
```
pip install omegaconf-cloud-resolvers[aws]
```

 * GCP:
```
pip install omegaconf-cloud-resolvers[gcp]
```

## Quickstart

The following is an introductory example using a secret stored in AWS Secrets Manager.

First create a secret in the AWS Secrets Manager. You can use the CLI:

```bash
aws secretsmanager create-secret --name secret_jwt --secret-string 'thiscouldbe.a.jwt'
```

```python
from omegaconf import OmegaConf
from omegaconf_cloud_resolvers import register_custom_resolvers
from omegaconf_cloud_resolvers.resolvers.aws import AWSSecretsManagerResolver

# Option A. Define an env var: `AWS_DEFAULT_PROFILE=<your-aws-profile>`
# If you do, there is no need to pass a Session to the PluginResolver

# Option B. Alternatively you can create a boto3 session and pass it to the `AWSSecretsManagerResolver`
# Check `.aws/config` to see what are your profiles.
#   from boto3 import Session
#   session = Session(profile_name="<your-aws-profile>")

# Define the custom resolver. The dict key is the name that you will use  in your config
resolvers = {
    "aws_secretsmanager": AWSSecretsManagerResolver(),
}
# Use CustomResolverInjector to declare the resolver. You cannot inject twice the same key.
register_custom_resolvers(**resolvers)

# The syntax is: <resolver-name>:<secret-name>
conf = OmegaConf.create({"secret": "${aws_secretsmanager:secret_jwt}"})
print("Your secret is:", conf["secret"])  # THAT IS AN ILLUSTRATIVE EXAMPLE, NEVER DO THIS IN PRODUCTION
```

## Roadmap

- [ ] Resolver for Azure Key Vault
- [ ] Support for older version for the AWS Secrets Manager Resolver
- [ ] Examples using AWS services - Lambda
- [ ] Examples using Google Cloud Platform services - Functions


# WARNING

This package is in a very early and experimental stage, use it under your own responsibility.

# Troubleshooting

* NoCredentialsError raised while resolving interpolation: Unable to locate credentials
  You might not have configured a default profile or provided with a session to a AWS Resolver.