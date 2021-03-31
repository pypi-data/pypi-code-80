import os, sys, boto3, botocore, datetime

class Authorization:
    def __init__(self, account_id, region_name, user_pool_client_id, user_pool_client_secret, identity_pool_id, cognito_provider_id):
        self.account_id = account_id
        self.region_name = region_name
        self.identity_pool_id = identity_pool_id
        self.cognito_provider_id = cognito_provider_id
        self.user_pool_client_id = user_pool_client_id
        self.user_pool_client_secret = user_pool_client_secret

    def refresh_token(self, username, refresh_token):
        client = boto3.client('cognito-idp', region_name=self.region_name)
        return client.initiate_auth(
            ClientId=self.user_pool_client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
                'SECRET_HASH': self.user_pool_client_secret
            }
        )

    def get_id(self, id_token):
        client = boto3.client('cognito-identity', region_name=self.region_name)
        return client.get_id(
            AccountId=self.account_id,
            IdentityPoolId=self.identity_pool_id,
            Logins={
                self.cognito_provider_id: os.environ['IDP_ID_TOKEN']
            }
        )

    def get_credentials_for_identity(self, id_token, role_arn):
        client = boto3.client('cognito-identity', region_name=self.region_name)
        id_response = Authorization.get_id(self, id_token)
        identity_id = id_response['IdentityId']
        return client.get_credentials_for_identity(
            IdentityId=identity_id,
            CustomRoleArn=role_arn,
            Logins={
                self.cognito_provider_id: os.environ['IDP_ID_TOKEN']
            }
        )

    def assume_role(role_arn, role_session_name):
        client = boto3.client('sts')
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name,
        )
        return response

    def assume_role_with_web_identity(role_arn, role_session_name, web_identity_token):
        client = boto3.client('sts')
        response = client.assume_role_with_web_identity(
            RoleArn=role_arn,
            RoleSessionName=role_session_name,
            WebIdentityToken=web_identity_token
        )
        return response

    def assumed_role_session(role_arn):
        base_session = boto3.session.Session()._session
        fetcher = botocore.credentials.AssumeRoleCredentialFetcher(
            client_creator=base_session.create_client,
            source_credentials=base_session.get_credentials(),
            role_arn=role_arn,
        )
        return botocore.credentials.DeferredRefreshableCredentials(
            method='assume-role',
            refresh_using=fetcher.fetch_credentials,
            time_fetcher=lambda: datetime.datetime.now(tzlocal())
        )
