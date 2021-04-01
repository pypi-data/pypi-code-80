from aws_cdk import (
    aws_codestarconnections as csc,
    core
)


class GithubConnection(core.Construct):
    connection = csc.CfnConnection

    def __init__(self, scope: core.Construct, id: str, connection_name: str, host_arn: str=None, *, **connection_args) -> None:
        super().__init__(scope, id)
        if host_arn:
            connection_args['host_arn'] = host_arn
        self.connection = csc.CfnConnection(
            self, 'github-connection',
            connection_name=connection_name,
            provider_type='GitHub',
            **connection_args
        )
