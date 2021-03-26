from os.path import join
from typing import TYPE_CHECKING, Optional, Dict

from rastervision.pipeline.config import Config, Field
from rastervision.pipeline.config import register_config

if TYPE_CHECKING:
    from rastervision.pipeline.pipeline import Pipeline  # noqa


@register_config('pipeline')
class PipelineConfig(Config):
    """Base class for configuring Pipelines.

    This should be subclassed to configure new Pipelines.
    """
    root_uri: str = Field(
        None, description='The root URI for output generated by the pipeline')
    rv_config: dict = Field(
        None,
        description='Used to store serialized RVConfig so pipeline can '
        'run in remote environment with the local RVConfig. This should '
        'not be set explicitly by users -- it is only used by the runner '
        'when running a remote pipeline.')
    plugin_versions: Optional[Dict[str, int]] = Field(
        None,
        description=
        ('Used to store a mapping of plugin module paths to the latest '
         'version number. This should not be set explicitly by users -- it is set '
         'automatically when serializing and saving the config to disk.'))

    def get_config_uri(self) -> str:
        """Get URI of serialized version of this PipelineConfig."""
        return join(self.root_uri, 'pipeline-config.json')

    def build(self, tmp_dir: str) -> 'Pipeline':
        """Return a pipeline based on this configuration.

        Subclasses should override this to return an instance of the
        corresponding subclass of Pipeline.

        Args:
            tmp_dir: root of any temporary directory to pass to pipeline
        """
        from rastervision.pipeline.pipeline import Pipeline  # noqa
        return Pipeline(self, tmp_dir)
