---
tags:
  - AWS
  - GCP
---

# Cloud Resolvers 

Each resolver uses the same interface but has unique features based on the service it connects to.
The next sections will cover important examples for each resolver.

## AWS 

### Prerequisites

The AWS resolvers in this package are built on top of the `boto3` library, which is the 
Amazon Web Services (AWS) SDK for Python.

#### Configuring AWS CLI (Optional)

If you are running this example from your local machine, ensure that you have configured your AWS credentials.

You might need to install the [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
if you don't have it yet.

After installing the AWS CLI, configure it with your credentials by running:

```bash
aws configure
```

This configuration is stored in the `~/.aws/credentials` and `~/.aws/config` files.

### Secrets Manager

#### Create a secret

!!! tip "Policy Check"
    
    If you have problems creating or accessing your secrets,  verify that you have the necessary permissions
    to access the AWS Secrets Manager. Review the [policies](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html)
    needed and ensure that your IAM user or role has the appropriate permissions.


You can create a secret using the AWS CLI or the AWS Management Console. 
Below is an example of how to create a secret using the AWS CLI:

```bash
aws secretsmanager create-secret --name db_secret_1 --secret-string '{"user":"user1","password":"mypassword"}'
```

#### Using the Secrets Manager Resolver

In this example, the `AWSSecretsManagerResolver` is used to fetch the secret named `db_secret_1` from AWS Secrets Manager.
The `infer_json` parameter is set to `True`, which means the resolver will attempt to parse the secret string into a
dictionary. This is of interest when the secret stores key:values pairs.
If `infer_json` is set to `False`, the secret will be returned as a plain string, which is useful if you store a secret 
string, like a JWT.

The following example shows how to use the AWS Secrets Manager resolver with default AWS credentials configuration.

```python 
from omegaconf import OmegaConf
from omegaconf_cloud_resolvers import register_custom_resolvers
from omegaconf_cloud_resolvers.resolvers.aws import AWSSecretsManagerResolver

resolvers = {
    "aws_secretsmanager": AWSSecretsManagerResolver(infer_json=True),
}
register_custom_resolvers(**resolvers)

conf = OmegaConf.create({
    "secret": "${aws_secretsmanager:db_secret_1}"
})
print(conf["user"])  # 'user1'
print(conf["password"])  # 'mypassword'
```

To check the class in depth, visit the reference page for [`AWSSecretsManagerResolver`](../api/resolvers/aws/secretsmanager.md).

### SSM Parameter Store

#### Create parameters

!!! tip "Policy Check"
    
    If you have problems creating or accessing your parameters, verify that you have the necessary permissions
    to access the SSM Parameter Store. Review the [policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-access.html)
    needed and ensure that your IAM user or role has the appropriate permissions.


You can create secrets using either the AWS Command Line Interface (CLI) or the AWS Management Console. 
Below are the instructions for using the CLI:

```bash
aws ssm put-parameter --name "/project1/env1/sec" --value "MySecureParameterValue" --type "SecureString"
aws ssm put-parameter --name "/project1/env1/list" --value "Value1,Value2,1,1.2" --type "StringList"
aws ssm put-parameter --name "/project1/env1/famA/a" --value "ValueA" --type "String"
aws ssm put-parameter --name "/project1/env1/famA/b" --value "ValueB" --type "SecureString"
```

#### Using the SSM Parameter Store Resolver

The `AWSParameterStoreResolver` is able to retrieve each one of the parameters types available: 

 * `String`: plain string, suitable for common values.
 * `StringList`: comma separated list of plain strings, suitable for a collection of non-encrypted values.
 * `SecureString`: encrypted string, suitable to store sensitive information.
  Use the argument `decrypt=True` (defaults to `True`) if you need the decrypted value stored, otherwise you will get
  the encrypted value.  

Another feature of the class is its ability to retrieve nested parameters. The options are: 
 * `/my/param`: retrieves one single value.
 * `/my/param/*`: retrieves `/my/param` and the first level hanging from `/my/param/`, i.e. `/my/param/a` and
   `/my/param/b`, as a dictionary: `{'param': ..., 'param/a': ...,'param/b': ...}`.
 * `/my/param/family`: retrieves `/my/param/family` and the all the parameters hanging from `/my/param/family`, i.e. `/my/param/family/a`,
   `/my/param/family/a/beta` and `/my/param/family/b`, as a dictionary: 
   `{'family': ..., 'family/a': ..., family/a/beta: ..., 'family/b': ...}`.

Lastly, `infer_types=True` will attempt to cast each value to the right type (). That could be of special interest when 
the parameter type is `StringList`.

The following case assumes that you have default configuration for your AWS credentials.

```python 
import boto3
from omegaconf import OmegaConf
from omegaconf_cloud_resolvers import register_custom_resolvers
from omegaconf_cloud_resolvers.resolvers.aws import AWSParameterStoreResolver

session = boto3.Session(profile_name="<my-profile>")

resolvers = {
    # Decrypts and infer the parameter. It will return a single value.
    "get_aws_param": AWSParameterStoreResolver(session=session, decrypt=True, infer_types=True),
    # This parameter is a list of elements, that does not require decryption. It will return a list[any]
    "get_aws_param_list": AWSParameterStoreResolver(session=session, decrypt=False, infer_types=True),
    # This parameter is a list of elements, that does not require decryption. It will return a list[str]
    "get_aws_param_list_str": AWSParameterStoreResolver(session=session, decrypt=False, infer_types=False),
}

register_custom_resolvers(**resolvers)

conf = OmegaConf.create({
    "sec_param":  "${get_aws_param:/project1/env1/sec}",
    "collection_param": "${get_aws_param:/project1/env1/famA/*}",
    "list_param": "${get_aws_param_list:/project1/env1/list}",
    "list_param_str": "${get_aws_param_list_str:/project1/env1/list}",
})

print(conf["sec_param"]) 
print(conf["collection_param"]) 
print(conf["list_param"])
print(conf["list_param_str"])
```

To check the class in depth, visit the reference page for [`AWSParameterStoreResolver`](../api/resolvers/aws/parameterstore.md).

## GCP

### Prerequisites 

If you are working on your local environment, ensure that you have the necessary permissions and tools installed to interact with 
Google Cloud Platform services, in this case, the Secret Manager. 

You will need the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated to your GCP account.
Set-up the environment [credentials](https://cloud.google.com/secret-manager/docs/authentication#client-libs) and 
make sure that you have the right access [permissions](https://cloud.google.com/secret-manager/docs/access-control).

If you want to set up Application Default Credentials (ADC), so your application automatically finds your environment 
credentials, review this [link](https://cloud.google.com/docs/authentication/provide-credentials-adc).

### Secret Manager

#### Create a Secret

Create a secret through the web or using the `gcloud` CLI, running the line below.

```bash
echo -n "This is a s3cr3t" | gcloud secrets create gcp-secret-001 --data-file=-
```

Also create a new version for this example.

```bash
echo -n "This is a s3cr3t v2" | gcloud secrets versions add gcp-secret-001 --data-file=-
```

#### Using the GCP Secret Manager Resolver

The typical way to access a  GCP secret is providing a combination of the project_id, the secret id and, optionally, the 
secret's version. That is supported by the resolver, allowing you to retrieve the secret providing a name under the 
following format:

 * `project/<project_id>/secrets/<secret_id>/versions/<version>`
 * `project/<project_id>/secrets/<secret_id>`: retrieve the latest version 
 * `secrets/<secret_id>/versions/<version>`: infer the project_id based on the default configuration
 * `secrets/<secret_id>`: infer the project_id based on the default configuration and retrieve the latest version  
 * `<secret_id>`: infer the project_id based on the default configuration and retrieve the latest version 

Assuming that you have the ADC, create a file `main.py` like the following:

```python
from omegaconf import OmegaConf
from omegaconf_cloud_resolvers import register_custom_resolvers
from omegaconf_cloud_resolvers.resolvers.gcp import GCPSecretManagerResolver

resolvers = {
    "get_gcp_secret": GCPSecretManagerResolver(),   # if you don't have the ADC, or you need to override the,
                                                    # provide: credentials and project_id
}
register_custom_resolvers(**resolvers)

conf = OmegaConf.create({
    "secret_01": "${get_gcp_secret:secrets/gcp-secret-001/versions/1}",
    "secret_02": "${get_gcp_secret:secrets/gcp-secret-001}",
    "secret_03": "${get_gcp_secret:gcp-secret-001}",
})

print(conf["secret_01"]) 
print(conf["secret_02"]) 
print(conf["secret_03"]) 
```
