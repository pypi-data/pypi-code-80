import typing
from aws_cdk import (
    aws_codebuild as cb,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
    aws_codestarconnections as csc,
    aws_s3,
    aws_secretsmanager as sm,
    aws_ssm,
    core
)
from . import (
    codebuild,
    sources
)


class Pipeline(cp.Pipeline):
    assembly: cp.Artifact
    __artifacts: dict={}
    __connections: dict={}

    def __init__(self, scope, id: str, *,
            connections: dict=None,
            **pipeline_args) -> None:

        if connections:
            self.connections = connections
        self.assembly = cp.Artifact('main')
        super().__init__(scope, id, **pipeline_args)

    @property
    def artifacts(self) -> dict:
        return self.__artifacts

    @artifacts.setter
    def artifacts(self, value: dict={}) -> None:
        self.__artifacts = value

    @property
    def connections(self) -> dict:
        return self.__connections

    @connections.setter
    def connections(self, connections: dict) -> None:
        for cname, connection_arn in connections.items():
            if connection_arn.startswith('aws:ssm:'):
                connection_arn = aws_ssm.StringParameter.value_from_lookup(
                    self, parameter_name=connection_arn.replace('aws:ssm:', '')
                )
            self.__connections[cname] = connection_arn

    def source(self, action_name: str=None, repository: typing.Union[str, sources.SourceRepositoryAttrs]=None, **source_args) -> cpa.BitBucketSourceAction:
        # Pick url / branch from the 'current' git clone
        if not repository:
            info = sources.git_repository_info()
            repository = f"{info.get('url')}@{info.get('branch')}"
        if isinstance(repository, str):
            repository = sources.git_url_split(repository)

        if not action_name:
            action_name = f"{repository['repo']}@{repository['branch']}"
        self.artifacts[action_name] = cp.Artifact()
        # repository['owner'] MUST match an existing self.connections
        connection_arn = self.connections[repository['owner']]
        return cpa.BitBucketSourceAction(
            connection_arn=connection_arn,
            output=self.artifacts[action_name],
            code_build_clone_output=True,
            **repository,
            action_name=action_name,
            **source_args
        )

    def build_project(self, id: str, *, specfile: str='buildspec.yml', **project_args) -> cb.Project:
        if not 'build_spec' in project_args:
            project_args['build_spec'] = codebuild.load_buildspec(specfile)
        return cb.Project(
            self, id,
            environment=cb.LinuxBuildImage.AMAZON_LINUX_2_3,
            **project_args
        )

    def build(self, action_name: str, sources: list=[], project_args: dict={}, **build_args) -> cpa.CodeBuildAction:
        self.artifacts[action_name] = [self.assembly]
        project = self.build_project(f"{action_name}-project", **project_args)

        if 'environment_variables' in build_args:
            build_args['environment_variables'] = self.process_environment_variables(
                environment_variables=build_args['environment_variables'], project=project
            )
        if sources:
            build_args['input'] = sources.pop(0)
            build_args['extra_inputs'] = sources

        action = cpa.CodeBuildAction(
            action_name=action_name,
            project=project,
            outputs=self.artifacts[action_name],
            **build_args
        )
        return action

    def process_environment_variables(self, environment_variables: dict, project: cb.Project) -> typing.Dict[str, cb.BuildEnvironmentVariable]:
        environment_variables = codebuild.buildenv(environment_variables)
        for name, var in environment_variables.items():
            if var.type == cb.BuildEnvironmentVariableType.SECRETS_MANAGER:
                sec = sm.Secret.from_secret_name_v2(self, f"{name}-secenv", secret_name=var.value)
                sec.grant_read(project)
        return environment_variables
