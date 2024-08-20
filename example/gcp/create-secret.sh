# Configure default credentials
# gcloud auth application-default login

# Create a secret
echo -n "This is a s3cr3t" | gcloud secrets create my-secret --data-file=-

echo -n "This is a s3cr3t v2" | gcloud secrets versions add gcp-secret-001 --data-file=-