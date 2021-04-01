import typing
from aws_cdk import (
    aws_codepipeline_actions,
    pipelines,
    core
)

from . import (
    codepipeline,
    sources
)

class PipelineStack(core.Stack):
    pipeline: codepipeline.Pipeline=None
    _pipelines: pipelines.CdkPipeline=None
    stages: typing.Dict[str, codepipeline.cp.IStage]={}

    def __init__(
            self, scope: core.Construct, id: str, *,
            pipeline_attr: dict={},
            connections: dict=None,
            auto_sourcebuild: bool=False,
            **kwargs) -> None:
        super().__init__(scope=scope, id=id, **kwargs)
        self.pipeline = codepipeline.Pipeline(self, 'pipeline', **pipeline_attr)
        if connections:
            self.pipeline.connections = connections
        if auto_sourcebuild:
            self.source()
            self.build()

    @property
    def cdk_pipelines(self) -> pipelines.CdkPipeline:
        if not self._pipelines:
            self._pipelines = pipelines.CdkPipeline(
                self, 'pipelines',
                cloud_assembly_artifact=self.pipeline.assembly,
                code_pipeline=self.pipeline
            )
        return self._pipelines

    def source(self, action_name: str=None, repository: typing.Union[str, sources.SourceRepositoryAttrs]=None, connections: dict=None) -> aws_codepipeline_actions.Action:
        """Add an action to watch a git reporitory/branch to the Source stage

        Args:
            action_name (str, optional): Name your source action (and artifact). Defaults to 'source'.
            repository (typing.Union[str, sources.SourceRepositoryAttrs], optional): The Git(hub) repository
              you are sourcing. Can be either an url or a dict with repo/owner/branch. Defaults to current repo/origin@branch.
            connections (dict, optional): AWS/Github org connections by name/codestar.connection_arn.

        Returns:
            aws_codepipeline_actions.Action: [description]
        """
        if connections:
            self.pipeline.connections = connections
        if 'Source' not in self.stages:
            self.stages['Source'] = self.pipeline.add_stage(stage_name='Source')
        action = self.pipeline.source(action_name=action_name, repository=repository)
        self.stages['Source'].add_action(action=action)
        return action

    def build(self, action_name: str=None, **build_args) -> aws_codepipeline_actions.Action:
        """Add an action to the Build stage

        Args:
            action_name (str, optional): Name your build action/artifact. Defaults to 'build'.

        Returns:
            aws_codepipeline_actions.Action: a Codepipeline / CodeBuildAction
        """
        if 'Build' not in self.stages:
            self.stages['Build'] = self.pipeline.add_stage(stage_name='Build')
        if 'input' not in build_args and 'sources' not in build_args:
            source = self.stages['Source'].actions[0].action_properties.action_name
            build_args['input'] = self.pipeline.artifacts[source]
            if not action_name:
                action_name = f"{source}-build"
        action = self.pipeline.build(action_name, **build_args)
        self.stages['Build'].add_action(action=action)
        return action
