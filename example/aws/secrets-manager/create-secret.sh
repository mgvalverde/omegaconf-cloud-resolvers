aws secretsmanager create-secret --name test_secret_1 --secret-string '{"username":"myuser","password":"mypassword"}'
aws secretsmanager create-secret --name test_secret_2 --secret-string 'thiscouldbe.a.jwt'
