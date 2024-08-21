aws ssm put-parameter --name "/project1/env1/param" --value "MyParameterValue" --type "String"
aws ssm put-parameter --name "/project1/env1/sec" --value "MySecureParameterValue" --type "SecureString"
aws ssm put-parameter --name "/project1/env1/list" --value "Value1,Value2,Value3" --type "StringList"