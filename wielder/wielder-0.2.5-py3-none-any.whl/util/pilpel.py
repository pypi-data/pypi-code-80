from boto3_session_cache import boto3_client

s3 = boto3_client(service_name='s3')
response = s3.list_buckets()

print(response)

with open("/tmp/rabbit.txt", "rb") as f:
    s3.upload_fileobj(f, "gichi", "rabbit.txt")

