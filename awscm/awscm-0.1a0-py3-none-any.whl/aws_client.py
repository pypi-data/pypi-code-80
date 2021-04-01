def get_aws_client(servicename, **kwargs):
    import boto3
    if kwargs.get('region'):
        region = kwargs['region']
        aws = boto3.client(servicename, region)
        return aws
    else:
        aws = boto3.client('glue')
        return aws