import trafaret as t

from datarobot import CustomModelVersion, ExecutionEnvironment, ExecutionEnvironmentVersion
from datarobot._experimental.models.custom_training_model import CustomTrainingModel
from datarobot.models.api_object import APIObject
from datarobot.utils import encode_utf8_if_py2
from datarobot.utils.pagination import unpaginate


class CustomTrainingBlueprint(APIObject):
    """A custom training blueprint.

    .. versionadded:: v2.21

    Attributes
    ----------
    id: str
        blueprint id
    custom_model: dict
        dict with 2 keys: `id` and `name`,
        where `id` is the ID of the custom model
        and `name` is the model name
    custom_model_version: dict
        dict with 2 keys: `id` and `label`,
        where `id` is the ID of the custom model version
        and `label` is the version label
    execution_environment: dict
        dict with 2 keys: `id` and `name`,
        where `id` is the ID of the execution environment
        and `name` is the environment name
    execution_environment_version: dict
        dict with 2 keys: `id` and `label`,
        where `id` is the ID of the execution environment version
        and `label` is the version label
    """

    _path = "customTrainingBlueprints/"
    _converter = t.Dict(
        {
            t.Key("blueprint_id") >> "id": t.String(),
            t.Key("custom_model"): t.Dict({t.Key("id"): t.String(), t.Key("name"): t.String()}),
            t.Key("custom_model_version"): t.Dict(
                {t.Key("id"): t.String(), t.Key("label"): t.String()}
            ),
            t.Key("execution_environment"): t.Dict(
                {t.Key("id"): t.String(), t.Key("name"): t.String()}
            ),
            t.Key("execution_environment_version"): t.Dict(
                {t.Key("id"): t.String(), t.Key("label"): t.String()}
            ),
            t.Key("training_history"): t.List(t.Dict()),
        }
    ).ignore_extra("*")

    def __init__(self, **kwargs):
        self._set_values(**kwargs)

    def __repr__(self):
        return encode_utf8_if_py2(u"{}({!r})".format(self.__class__.__name__, self.id))

    def _set_values(
        self,
        id,
        custom_model,
        custom_model_version,
        execution_environment,
        execution_environment_version,
        training_history,
        project_id=None,
        filenames=None,
    ):
        self.id = id
        self.custom_model = custom_model
        self.custom_model_version = custom_model_version
        self.execution_environment = execution_environment
        self.execution_environment_version = execution_environment_version
        self.training_history = training_history
        self.project_id = project_id
        self.filenames = filenames

    @classmethod
    def create(
        cls,
        custom_model_id,
        environment_id=None,
        custom_model_version_id=None,
        environment_version_id=None,
    ):
        """Create a custom learning blueprint.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            the id of the custom model
        environment_id: Optional[str]
            the id of the execution environment
            If specified, the environment will be used "as-is"; if the custom model version
            has dependencies, they will not be installed at runtime.
        custom_model_version_id: Optional[str]
            the id of the custom model version
        environment_version_id: Optional[str]
            the id of the execution environment version. If version is none, what happens?


        if custom_model_id is provided, latest version will be used.
        if custom_model_version_id is provided, custom_model_id will be looked up
        One must be provided
        same for execution environments

        Returns
        -------
        CustomTrainingBlueprint
            created custom learning blueprint

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        if not custom_model_version_id:
            model = CustomTrainingModel.get(custom_model_id=custom_model_id)
            custom_model_version_id = model.latest_version.id

        payload = {
            "custom_model_id": custom_model_id,
            "custom_model_version_id": custom_model_version_id,
        }
        if environment_id:
            payload.update(
                {
                    "environment_id": environment_id,
                    "environment_version_id": environment_version_id,
                }
            )
        response = cls._client.post(cls._path, data=payload)
        return cls.from_server_data(response.json())

    @classmethod
    def create_from_scratch(cls, name, environment_dir, training_code_files, target_type):
        desc = "Generated from python client"
        # Make environment
        ee = ExecutionEnvironment.create(
            name=name + "-environment", description=desc, programming_language="python"
        )
        ExecutionEnvironmentVersion.create(
            str(ee.id), environment_dir, description=desc,
        )

        # Make custom model
        cm = CustomTrainingModel.create(
            name=name + "-model", target_type=target_type, description=desc
        )
        cmv = CustomModelVersion.create_clean(
            custom_model_id=cm.id, base_environment_id=ee.id, files=training_code_files
        )

        blueprint = cls.create(custom_model_id=cm.id, custom_model_version_id=cmv.id)
        blueprint.filenames = training_code_files
        return blueprint

    @classmethod
    def create_from_dropin(
        cls, model_name, dropin_env_id, target_type, training_code_files=None, folder_path=None
    ):
        new_custom_training_model = CustomTrainingModel.create(
            name=model_name, target_type=target_type
        )
        CustomModelVersion.create_clean(
            new_custom_training_model.id,
            base_environment_id=dropin_env_id,
            files=training_code_files,
            folder_path=folder_path,
        )
        blueprint = cls.create(custom_model_id=new_custom_training_model.id)
        blueprint.filenames = training_code_files
        return blueprint

    @classmethod
    def list(cls):
        """List custom learning blueprints.

        .. versionadded:: v2.21

        Returns
        -------
        List[CustomLearningBlueprint]
            a list of custom learning blueprints

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(cls._path, {}, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, blueprint_id):
        """Get custom learning blueprint by id.

        .. versionadded:: v2.21

        Parameters
        ----------
        blueprint_id: str
            the id of the custom learning blueprint

        Returns
        -------
        CustomTrainingBlueprint
            retrieved custom learning blueprint

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = "{}{}/".format(cls._path, blueprint_id)
        return cls.from_location(path)

    def with_updated_code(self, filenames=None):
        filenames_to_use = filenames
        if filenames is not None:
            self.filenames = filenames
        elif filenames is None and self.filenames is not None:
            filenames_to_use = self.filenames
        else:
            raise ValueError("Please provide all model filenames")

        cm_id = self.custom_model["id"]
        cmv = CustomModelVersion.create_clean(
            custom_model_id=cm_id,
            files=filenames_to_use,
            base_environment_id=self.execution_environment["id"],
        )
        self.custom_model_version = {"id": cmv.id, "label": cmv.label}
        payload = dict(custom_model_id=cm_id, custom_model_version_id=cmv.id)
        response = self._client.post(self._path, data=payload)
        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))
        return self
