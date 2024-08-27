# Examples

## AWS

Make sure that you have permissions to access the secret, and that you are logged in.

 * Access from AWS resources (role granted permissions):
   Make sure that the attached role has the right permissions to access the secret. 
   Note: watch out any other potential resource like KMS key, in case that you chose a custom encryption key.  

 * Access from local environment
   A. If using default session. Make sure that you have configured properly the right profile.
   B. Provide a custom `boto3.Session` to the `AWSSecretsManagerResolver` or `AWSParameterStoreResolver`. 

## GCP

 * Access from GCP resources (role granted permissions): 
   Make sure that the attached role has the right permissions to access the secret. 

 * Access from local environment
   A. Configure the Application Default Credentials. This will allow the GCPSecretManagerMixin to know what `credentials` and `project_id` to use.

```python
from omegaconf_cloud_resolvers import CustomResolverInjector
from omegaconf_cloud_resolvers.resolvers.gcp import GCPSecretManagerResolver

resolvers = {
   "get_gcp_secret": GCPSecretManagerResolver(),
}
injector = CustomResolverInjector.inject_resolvers(**resolvers)
```
   B. Provide a custom `credentials` and `project_id` to the `GCPSecretManagerMixin`.

```python
from omegaconf_cloud_resolvers import CustomResolverInjector
from omegaconf_cloud_resolvers.resolvers.gcp import GCPSecretManagerResolver

resolvers = {
   "get_gcp_secret": GCPSecretManagerResolver(),
}
injector = CustomResolverInjector.inject_resolvers(**resolvers)
```