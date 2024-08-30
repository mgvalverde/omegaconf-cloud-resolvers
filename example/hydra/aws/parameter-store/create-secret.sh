aws ssm put-parameter --name "/project1/env1/param" --value "MyParameterValue" --type "String"
aws ssm put-parameter --name "/project1/env1/sec" --value "MySecureParameterValue" --type "SecureString"
aws ssm put-parameter --name "/project1/env1/list" --value "Value1,Value2,1,1.2" --type "StringList"
aws ssm put-parameter --name "/project1/env1/param2" --value "MyParameterValue" --type "String"
aws ssm put-parameter --name "/project1/env2/param1" --value "MyParameterValue" --type "String"
aws ssm put-parameter --name "/project1/env2/param1" --value "MyParameterValue.v2" --type "String" --overwrite
aws ssm put-parameter --name "/project1/env2/param1" --value "MyParameterValue.v3" --type "String" --overwrite
aws ssm put-parameter --name "/project1/env2/param1/a" --value "SubMyParameterA" --type "String" --overwrite
aws ssm put-parameter --name "/project1/env2/param1/a/alpha" --value "SubMyParameterAlpha" --type "String" --overwrite
aws ssm put-parameter --name "/project1/env2/param1/b" --value "SubMyParameterB" --type "String" --overwrite
aws ssm put-parameter --name "/project1/env2/param2" --value "SubMyParameterB" --type "SecureString" --overwrite