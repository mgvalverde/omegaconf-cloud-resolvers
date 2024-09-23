# Configure default credentials
az login
az group create --name <ResourceGroupName> --location germanywestcentral
az keyvault create --name <ConfigVaulName> --resource-group <ResourceGroupName> --location germanywestcentral
az keyvault secret set --vault-name <ConfigVaulName> --name MySecret --value "This is a s3cr3t"
az keyvault secret set --vault-name <ConfigVaulName> --name MySecret --value "This is a s3cr3t v2"

# In case of error creating the secret:
# https://learn.microsoft.com/en-us/answers/questions/1370440/azure-keyvault-the-operation-is-not-allowed-by-rba
