from __future__ import annotations

import importlib
import re
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, TypeVar

from flytekit.common.tasks.raw_container import _get_container_definition
from flytekit.core.base_task import PythonTask
from flytekit.core.context_manager import FlyteContext, ImageConfig, SerializationSettings
from flytekit.core.resources import Resources, ResourceSpec
from flytekit.core.tracker import TrackedInstance
from flytekit.loggers import logger
from flytekit.models import task as _task_model
from flytekit.models.security import Secret, SecurityContext

T = TypeVar("T")


class FlyteTrackedABC(type(TrackedInstance), type(ABC)):
    """
    This class exists because if you try to inherit from abc.ABC and TrackedInstance by itself, you'll get the
    well-known ``TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass
    of the metaclasses of all its bases`` error.
    """


class PythonAutoContainerTask(PythonTask[T], metaclass=FlyteTrackedABC):
    """
    A Python AutoContainer task should be used as the base for all extensions that want the user's code to be in the
    container and the container information to be automatically captured.
    This base will auto configure the image and image version to be used for all its derivatives.

    If you are looking to extend, you might prefer to use ``PythonFunctionTask`` or ``PythonInstanceTask``
    """

    def __init__(
        self,
        name: str,
        task_config: T,
        task_type="python-task",
        container_image: Optional[str] = None,
        requests: Optional[Resources] = None,
        limits: Optional[Resources] = None,
        environment: Optional[Dict[str, str]] = None,
        task_resolver: Optional[TaskResolverMixin] = None,
        secret_requests: Optional[List[Secret]] = None,
        **kwargs,
    ):
        """
        :param name: unique name for the task, usually the function's module and name.
        :param task_config: Configuration object for Task. Should be a unique type for that specific Task
        :param task_type: String task type to be associated with this Task
        :param container_image: String FQN for the image.
        :param requests: custom resource request settings.
        :param limits: custom resource limit settings.
        :param environment: Environment variables you want the task to have when run.
        :param task_resolver: Custom resolver - will pick up the default resolver if empty, or the resolver set
          in the compilation context if one is set.
        :param List[Secret] secret_requests: Secrets that are requested by this container execution. These secrets will
                                           be mounted based on the configuration in the Secret and available through
                                           the SecretManager using the name of the secret as the group
                                           Ideally the secret keys should also be semi-descriptive.
                                           The key values will be available from runtime, if the backend is configured
                       to provide secrets and if secrets are available in the configured secrets store.
                       Possible options for secret stores are
                        - `Vault <https://www.vaultproject.io/>`,
                        - `Confidant <https://lyft.github.io/confidant/>`,
                        - `Kube secrets <https://kubernetes.io/docs/concepts/configuration/secret/>`
                        - `AWS Parameter store <https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html>`_
                        etc
        """
        sec_ctx = None
        if secret_requests:
            for s in secret_requests:
                if not isinstance(s, Secret):
                    raise AssertionError(f"Secret {s} should be of type flytekit.Secret, received {type(s)}")
            sec_ctx = SecurityContext(secrets=secret_requests)
        super().__init__(
            task_type=task_type,
            name=name,
            task_config=task_config,
            security_ctx=sec_ctx,
            **kwargs,
        )
        self._container_image = container_image
        # TODO(katrogan): Implement resource overrides
        self._resources = ResourceSpec(
            requests=requests if requests else Resources(), limits=limits if limits else Resources()
        )
        self._environment = environment

        compilation_state = FlyteContext.current_context().compilation_state
        if compilation_state and compilation_state.task_resolver:
            if task_resolver:
                logger.info(
                    f"Not using the passed in task resolver {task_resolver} because one found in compilation context"
                )
            self._task_resolver = compilation_state.task_resolver
            if self._task_resolver.task_name(self) is not None:
                self._name = self._task_resolver.task_name(self)
        else:
            self._task_resolver = task_resolver or default_task_resolver

    @property
    def task_resolver(self) -> TaskResolverMixin:
        return self._task_resolver

    @property
    def container_image(self) -> Optional[str]:
        return self._container_image

    @property
    def resources(self) -> ResourceSpec:
        return self._resources

    @abstractmethod
    def get_command(self, settings: SerializationSettings) -> List[str]:
        pass

    def get_container(self, settings: SerializationSettings) -> _task_model.Container:
        env = {**settings.env, **self.environment} if self.environment else settings.env
        return _get_container_definition(
            image=get_registerable_container_image(self.container_image, settings.image_config),
            command=[],
            args=self.get_command(settings=settings),
            data_loading_config=None,
            environment=env,
            storage_request=self.resources.requests.storage,
            cpu_request=self.resources.requests.cpu,
            gpu_request=self.resources.requests.gpu,
            memory_request=self.resources.requests.mem,
            storage_limit=self.resources.limits.storage,
            cpu_limit=self.resources.limits.cpu,
            gpu_limit=self.resources.limits.gpu,
            memory_limit=self.resources.limits.mem,
        )


class TaskResolverMixin(object):
    """
    Flytekit tasks interact with the Flyte platform very, very broadly in two steps. They need to be uploaded to Admin,
    and then they are run by the user upon request (either as a single task execution or as part of a workflow). In any
    case, at execution time, the container image containing the task needs to be spun up again (for container tasks at
    least which most tasks are) at which point the container needs to know which task it's supposed to run and
    how to rehydrate the task object.

    For example, the serialization of a simple task ::

        # in repo_root/workflows/example.py
        @task
        def t1(...) -> ...: ...

    might result in a container with arguments like ::

        pyflyte-execute --inputs s3://path/inputs.pb --output-prefix s3://outputs/location \
        --raw-output-data-prefix /tmp/data \
        --resolver flytekit.core.python_auto_container.default_task_resolver \
        -- \
        task-module repo_root.workflows.example task-name t1

    At serialization time, the container created for the task will start out automatically with the ``pyflyte-execute``
    bit, along with the requisite input/output args and the offloaded data prefix. Appended to that will be two things,

    #. the ``location`` of the task's task resolver, followed by two dashes, followed by
    #. the arguments provided by calling the ``loader_args`` function below.

    The ``default_task_resolver`` declared below knows that ::

    * When ``loader_args`` is called on a task, to look up the module the task is in, and the name of the task (the
      key of the task in the module, either the function name, or the variable it was assigned to).
    * When ``load_task`` is called, it interprets the first part of the command as the module to call
    ``importlib.import_module`` on, and then looks for a key ``t1``.

    This is just the default behavior. Users should feel free to implement their own resolvers.
    """

    @property
    @abstractmethod
    def location(self) -> str:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def load_task(self, loader_args: List[str]) -> PythonAutoContainerTask:
        """
        Given the set of identifier keys, should return one Python Task or raise an error if not found
        """
        pass

    @abstractmethod
    def loader_args(self, settings: SerializationSettings, t: PythonAutoContainerTask) -> List[str]:
        """
        Return a list of strings that can help identify the parameter Task
        """
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[PythonAutoContainerTask]:
        """
        Future proof method. Just making it easy to access all tasks (Not required today as we auto register them)
        """
        pass

    def task_name(self, t: PythonAutoContainerTask) -> Optional[str]:
        """
        Overridable function that can optionally return a custom name for a given task
        """
        return None


class DefaultTaskResolver(TrackedInstance, TaskResolverMixin):
    """
    Please see the notes in the TaskResolverMixin as it describes this default behavior.
    """

    def name(self) -> str:
        return "DefaultTaskResolver"

    def load_task(self, loader_args: List[str]) -> PythonAutoContainerTask:
        _, task_module, _, task_name, *_ = loader_args

        task_module = importlib.import_module(task_module)
        task_def = getattr(task_module, task_name)
        return task_def

    def loader_args(self, settings: SerializationSettings, task: PythonAutoContainerTask) -> List[str]:
        from flytekit.core.python_function_task import PythonFunctionTask

        if isinstance(task, PythonFunctionTask):
            return [
                "task-module",
                task.task_function.__module__,
                "task-name",
                task.task_function.__name__,
            ]
        if isinstance(task, TrackedInstance):
            return [
                "task-module",
                task.instantiated_in,
                "task-name",
                task.lhs,
            ]

    def get_all_tasks(self) -> List[PythonAutoContainerTask]:
        raise Exception("should not be needed")


default_task_resolver = DefaultTaskResolver()


def get_registerable_container_image(img: Optional[str], cfg: ImageConfig) -> str:
    """
    :param img: Configured image
    :param cfg: Registration configuration
    :return:
    """
    if img is not None and img != "":
        matches = _IMAGE_REPLACE_REGEX.findall(img)
        if matches is None or len(matches) == 0:
            return img
        for m in matches:
            if len(m) < 3:
                raise AssertionError(
                    "Image specification should be of the form <fqn>:<tag> OR <fqn>:{{.image.default.version}} OR "
                    f"{{.image.xyz.fqn}}:{{.image.xyz.version}} OR {{.image.xyz}} - Received {m}"
                )
            replace_group, name, attr = m
            if name is None or name == "":
                raise AssertionError(f"Image format is incorrect {m}")
            img_cfg = cfg.find_image(name)
            if img_cfg is None:
                raise AssertionError(f"Image Config with name {name} not found in the configuration")
            if attr == "version":
                if img_cfg.tag is not None:
                    img = img.replace(replace_group, img_cfg.tag)
                else:
                    img = img.replace(replace_group, cfg.default_image.tag)
            elif attr == "fqn":
                img = img.replace(replace_group, img_cfg.fqn)
            elif attr == "":
                img = img.replace(replace_group, img_cfg.full)
            else:
                raise AssertionError(f"Only fqn and version are supported replacements, {attr} is not supported")
        return img
    return f"{cfg.default_image.fqn}:{cfg.default_image.tag}"


# Matches {{.image.<name>.<attr>}}. A name can be either 'default' indicating the default image passed during
# serialization or it can be a custom name for an image that must be defined in the config section Images. An attribute
# can be either 'fqn', 'version' or non-existent.
# fqn will access the fully qualified name of the image (e.g. registry/imagename:version -> registry/imagename)
# version will access the version part of the image (e.g. registry/imagename:version -> version)
# With empty attribute, it'll access the full image path (e.g. registry/imagename:version -> registry/imagename:version)
_IMAGE_REPLACE_REGEX = re.compile(r"({{\s*\.image[s]?(?:\.([a-zA-Z]+))(?:\.([a-zA-Z]+))?\s*}})", re.IGNORECASE)
