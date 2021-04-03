from boto3_session_cache import boto3_client

ec2 = boto3_client(service_name='ec2')
response = ec2.describe_instances()
print(response)
