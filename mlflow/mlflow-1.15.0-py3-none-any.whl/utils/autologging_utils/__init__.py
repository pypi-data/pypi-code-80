import os
import abc
import importlib
import inspect
import itertools
import functools
import warnings
import logging
import time
import contextlib
import uuid
import yaml
from collections import namedtuple
from contextlib import contextmanager
from abc import abstractmethod
from distutils.version import LooseVersion
from pkg_resources import resource_filename

import mlflow
from mlflow.entities.run_status import RunStatus
from mlflow.entities import Metric
from mlflow.tracking.client import MlflowClient
from mlflow.utils.autologging_utils.logging_and_warnings import (
    set_mlflow_events_and_warnings_behavior_globally,
    set_non_mlflow_warnings_behavior_for_current_thread,
)
from mlflow.utils import gorilla
from mlflow.utils.mlflow_tags import MLFLOW_AUTOLOGGING
from mlflow.utils.validation import MAX_METRICS_PER_BATCH


INPUT_EXAMPLE_SAMPLE_ROWS = 5
ENSURE_AUTOLOGGING_ENABLED_TEXT = (
    "please ensure that autologging is enabled before constructing the dataset."
)
_AUTOLOGGING_TEST_MODE_ENV_VAR = "MLFLOW_AUTOLOGGING_TESTING"

# Dict mapping integration name to its config.
AUTOLOGGING_INTEGRATIONS = {}

_logger = logging.getLogger(__name__)


def try_mlflow_log(fn, *args, **kwargs):
    """
    Catch exceptions and log a warning to avoid autolog throwing.
    """
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        if _is_testing():
            raise
        else:
            warnings.warn("Logging to MLflow failed: " + str(e), stacklevel=2)


def log_fn_args_as_params(fn, args, kwargs, unlogged=[]):  # pylint: disable=W0102
    """
    Log parameters explicitly passed to a function.

    :param fn: function whose parameters are to be logged
    :param args: arguments explicitly passed into fn. If `fn` is defined on a class,
                 `self` should not be part of `args`; the caller is responsible for
                 filtering out `self` before calling this function.
    :param kwargs: kwargs explicitly passed into fn
    :param unlogged: parameters not to be logged
    :return: None
    """
    param_spec = inspect.signature(fn).parameters
    # Filter out `self` from the signature under the assumption that it is not contained
    # within the specified `args`, as stipulated by the documentation
    relevant_params = [param for param in param_spec.values() if param.name != "self"]

    # Fetch the parameter names for specified positional arguments from the function
    # signature & create a mapping from positional argument name to specified value
    params_to_log = {
        param_info.name: param_val
        for param_info, param_val in zip(list(relevant_params)[: len(args)], args)
    }
    # Add all user-specified keyword arguments to the set of parameters to log
    params_to_log.update(kwargs)
    # Add parameters that were not explicitly specified by the caller to the mapping,
    # using their default values
    params_to_log.update(
        {
            param.name: param.default
            for param in list(relevant_params)[len(args) :]
            if param.name not in kwargs
        }
    )
    # Filter out any parameters that should not be logged, as specified by the `unlogged` parameter
    params_to_log = {key: value for key, value in params_to_log.items() if key not in unlogged}
    try_mlflow_log(mlflow.log_params, params_to_log)


def _update_wrapper_extended(wrapper, wrapped):
    """
    Update a `wrapper` function to look like the `wrapped` function. This is an extension of
    `functools.update_wrapper` that applies the docstring *and* signature of `wrapped` to
    `wrapper`, producing a new function.

    :return: A new function with the same implementation as `wrapper` and the same docstring
             & signature as `wrapped`.
    """
    updated_wrapper = functools.update_wrapper(wrapper, wrapped)
    # Assign the signature of the `wrapped` function to the updated wrapper function.
    # Certain frameworks may disallow signature inspection, causing `inspect.signature()` to throw.
    # One such example is the `tensorflow.estimator.Estimator.export_savedmodel()` function
    try:
        updated_wrapper.__signature__ = inspect.signature(wrapped)
    except Exception:
        _logger.debug("Failed to restore original signature for wrapper around %s", wrapped)
    return updated_wrapper


def _wrap_patch(destination, name, patch, settings=None):
    """
    Apply a patch while preserving the attributes (e.g. __doc__) of an original function.

    :param destination: Patch destination
    :param name: Name of the attribute at the destination
    :param patch: Patch function
    :param settings: Settings for gorilla.Patch
    """
    if settings is None:
        settings = gorilla.Settings(allow_hit=True, store_hit=True)

    original = getattr(destination, name)
    wrapped = _update_wrapper_extended(patch, original)

    patch = gorilla.Patch(destination, name, wrapped, settings=settings)
    gorilla.apply(patch)


class _InputExampleInfo:
    """
    Stores info about the input example collection before it is needed.

    For example, in xgboost and lightgbm, an InputExampleInfo object is attached to the dataset,
    where its value is read later by the train method.

    Exactly one of input_example or error_msg should be populated.
    """

    def __init__(self, input_example=None, error_msg=None):
        self.input_example = input_example
        self.error_msg = error_msg


def resolve_input_example_and_signature(
    get_input_example, infer_model_signature, log_input_example, log_model_signature, logger
):
    """
    Handles the logic of calling functions to gather the input example and infer the model
    signature.

    :param get_input_example: function which returns an input example, usually sliced from a
                              dataset. This function can raise an exception, its message will be
                              shown to the user in a warning in the logs.
    :param infer_model_signature: function which takes an input example and returns the signature
                                  of the inputs and outputs of the model. This function can raise
                                  an exception, its message will be shown to the user in a warning
                                  in the logs.
    :param log_input_example: whether to log errors while collecting the input example, and if it
                              succeeds, whether to return the input example to the user. We collect
                              it even if this parameter is False because it is needed for inferring
                              the model signature.
    :param log_model_signature: whether to infer and return the model signature.
    :param logger: the logger instance used to log warnings to the user during input example
                   collection and model signature inference.

    :return: A tuple of input_example and signature. Either or both could be None based on the
             values of log_input_example and log_model_signature.
    """

    input_example = None
    input_example_user_msg = None
    input_example_failure_msg = None
    if log_input_example or log_model_signature:
        try:
            input_example = get_input_example()
        except Exception as e:
            input_example_failure_msg = str(e)
            input_example_user_msg = "Failed to gather input example: " + str(e)

    model_signature = None
    model_signature_user_msg = None
    if log_model_signature:
        try:
            if input_example is None:
                raise Exception(
                    "could not sample data to infer model signature: " + input_example_failure_msg
                )
            model_signature = infer_model_signature(input_example)
        except Exception as e:
            model_signature_user_msg = "Failed to infer model signature: " + str(e)

    if log_input_example and input_example_user_msg is not None:
        logger.warning(input_example_user_msg)
    if log_model_signature and model_signature_user_msg is not None:
        logger.warning(model_signature_user_msg)

    return input_example if log_input_example else None, model_signature


class BatchMetricsLogger:
    """
    The BatchMetricsLogger will log metrics in batch against an mlflow run.
    If run_id is passed to to constructor then all recording and logging will
    happen against that run_id.
    If no run_id is passed into constructor, then the run ID will be fetched
    from `mlflow.active_run()` each time `record_metrics()` or `flush()` is called; in this
    case, callers must ensure that an active run is present before invoking
    `record_metrics()` or `flush()`.
    """

    def __init__(self, run_id=None):
        self.run_id = run_id

        # data is an array of Metric objects
        self.data = []
        self.total_training_time = 0
        self.total_log_batch_time = 0
        self.previous_training_timestamp = None

    def flush(self):
        """
        The metrics accumulated by BatchMetricsLogger will be batch logged to an MLFlow run.
        """
        self._timed_log_batch()
        self.data = []

    def _timed_log_batch(self):
        if self.run_id is None:
            # Retrieving run_id from active mlflow run.
            current_run_id = mlflow.active_run().info.run_id
        else:
            current_run_id = self.run_id

        start = time.time()
        metrics_slices = [
            self.data[i : i + MAX_METRICS_PER_BATCH]
            for i in range(0, len(self.data), MAX_METRICS_PER_BATCH)
        ]
        for metrics_slice in metrics_slices:
            try_mlflow_log(MlflowClient().log_batch, run_id=current_run_id, metrics=metrics_slice)
        end = time.time()
        self.total_log_batch_time += end - start

    def _should_flush(self):
        target_training_to_logging_time_ratio = 10
        if (
            self.total_training_time
            >= self.total_log_batch_time * target_training_to_logging_time_ratio
        ):
            return True

        return False

    def record_metrics(self, metrics, step=None):
        """
        Submit a set of metrics to be logged. The metrics may not be immediately logged, as this
        class will batch them in order to not increase execution time too much by logging
        frequently.

        :param metrics: dictionary containing key, value pairs of metrics to be logged.
        :param step: the training step that the metrics correspond to.
        """
        current_timestamp = time.time()
        if self.previous_training_timestamp is None:
            self.previous_training_timestamp = current_timestamp

        training_time = current_timestamp - self.previous_training_timestamp

        self.total_training_time += training_time

        # log_batch() requires step to be defined. Therefore will set step to 0 if not defined.
        if step is None:
            step = 0

        for key, value in metrics.items():

            self.data.append(Metric(key, value, int(current_timestamp * 1000), step))

        if self._should_flush():
            self.flush()

        self.previous_training_timestamp = current_timestamp


@contextlib.contextmanager
def batch_metrics_logger(run_id):
    """
    Context manager that yields a BatchMetricsLogger object, which metrics can be logged against.
    The BatchMetricsLogger keeps metrics in a list until it decides they should be logged, at
    which point the accumulated metrics will be batch logged. The BatchMetricsLogger ensures
    that logging imposes no more than a 10% overhead on the training, where the training is
    measured by adding up the time elapsed between consecutive calls to record_metrics.

    If logging a batch fails, a warning will be emitted and subsequent metrics will continue to
    be collected.

    Once the context is closed, any metrics that have yet to be logged will be logged.

    :param run_id: ID of the run that the metrics will be logged to.
    """

    batch_metrics_logger = BatchMetricsLogger(run_id)
    yield batch_metrics_logger
    batch_metrics_logger.flush()


def _check_version_in_range(ver, min_ver, max_ver):
    return LooseVersion(min_ver) <= LooseVersion(ver) <= LooseVersion(max_ver)


def _load_version_file_as_dict():
    version_file_path = resource_filename(__name__, "../../ml-package-versions.yml")
    with open(version_file_path) as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


_module_version_info_dict = _load_version_file_as_dict()


# A map FLAVOR_NAME -> a tuple of (dependent_module_name, key_in_module_version_info_dict)
_cross_tested_flavor_to_module_name_and_module_key = {
    "fastai": ("fastai", "fastai-1.x"),
    "gluon": ("mxnet", "gluon"),
    "keras": ("keras", "keras"),
    "lightgbm": ("lightgbm", "lightgbm"),
    "statsmodels": ("statsmodels", "statsmodels"),
    "tensorflow": ("tensorflow", "tensorflow"),
    "xgboost": ("xgboost", "xgboost"),
    "sklearn": ("sklearn", "sklearn"),
    "pytorch": ("pytorch_lightning", "pytorch-lightning"),
}


def _get_min_max_version_and_pip_release(module_key):
    min_version = _module_version_info_dict[module_key]["autologging"]["minimum"]
    max_version = _module_version_info_dict[module_key]["autologging"]["maximum"]
    pip_release = _module_version_info_dict[module_key]["package_info"]["pip_release"]
    return min_version, max_version, pip_release


def _is_autologging_integration_supported(flavor_name):
    """
    :return: True if the flavor's associated package version is compatible with mlflow,
             False otherwise.
    """
    module_name, module_key = _cross_tested_flavor_to_module_name_and_module_key[flavor_name]
    actual_version = importlib.import_module(module_name).__version__
    min_version, max_version, _ = _get_min_max_version_and_pip_release(module_key)
    return _check_version_in_range(actual_version, min_version, max_version)


def _gen_autologging_package_version_requirements_doc(flavor_name):
    """
    :return: A document note string saying the compatibility for the flavor's associated package
             versions.
    """
    _, module_key = _cross_tested_flavor_to_module_name_and_module_key[flavor_name]
    min_ver, max_ver, pip_release = _get_min_max_version_and_pip_release(module_key)
    required_pkg_versions = "``{min_ver}`` <= ``{pip_release}`` <= ``{max_ver}``".format(
        min_ver=min_ver, pip_release=pip_release, max_ver=max_ver
    )

    return (
        "    .. Note:: Autologging is known to be compatible with the following package versions: "
        + required_pkg_versions
        + ". Autologging may not succeed when used with package versions outside of this range."
        + "\n\n"
    )


def _check_and_log_warning_for_unsupported_integration(flavor_name):
    """
    When autologging enabled disable_for_unsupported_versions disabled, check whether the flavor
    package version is compatible with mlflow, if not compatible, log a warning message.
    """
    if (
        flavor_name in _cross_tested_flavor_to_module_name_and_module_key
        and not get_autologging_config(flavor_name, "disable", True)
        and not get_autologging_config(flavor_name, "disable_for_unsupported_versions", False)
        and not _is_autologging_integration_supported(flavor_name)
    ):
        _logger.warning(
            "You are using an unsupported version of %s. If you encounter errors during "
            "autologging, try upgrading / downgrading %s to a supported version, or try "
            "upgrading MLflow.",
            flavor_name,
            flavor_name,
        )


def autologging_integration(name):
    """
    **All autologging integrations should be decorated with this wrapper.**

    Wraps an autologging function in order to store its configuration arguments. This enables
    patch functions to broadly obey certain configurations (e.g., disable=True) without
    requiring specific logic to be present in each autologging integration.
    """

    def validate_param_spec(param_spec):
        if "disable" not in param_spec or param_spec["disable"].default is not False:
            raise Exception(
                "Invalid `autolog()` function for integration '{}'. `autolog()` functions"
                " must specify a 'disable' argument with default value 'False'".format(name)
            )
        elif "silent" not in param_spec or param_spec["silent"].default is not False:
            raise Exception(
                "Invalid `autolog()` function for integration '{}'. `autolog()` functions"
                " must specify a 'silent' argument with default value 'False'".format(name)
            )

    def wrapper(_autolog):
        param_spec = inspect.signature(_autolog).parameters
        validate_param_spec(param_spec)

        AUTOLOGGING_INTEGRATIONS[name] = {}
        default_params = {param.name: param.default for param in param_spec.values()}

        def autolog(*args, **kwargs):
            config_to_store = dict(default_params)
            config_to_store.update(
                {param.name: arg for arg, param in zip(args, param_spec.values())}
            )
            config_to_store.update(kwargs)
            AUTOLOGGING_INTEGRATIONS[name] = config_to_store

            is_silent_mode = get_autologging_config(name, "silent", False)
            # Reroute non-MLflow warnings encountered during autologging enablement to an
            # MLflow event logger, and enforce silent mode if applicable (i.e. if the corresponding
            # autologging integration was called with `silent=True`)
            with set_mlflow_events_and_warnings_behavior_globally(
                # MLflow warnings emitted during autologging setup / enablement are likely
                # actionable and relevant to the user, so they should be emitted as normal
                # when `silent=False`. For reference, see recommended warning and event logging
                # behaviors from https://docs.python.org/3/howto/logging.html#when-to-use-logging
                reroute_warnings=False,
                disable_event_logs=is_silent_mode,
                disable_warnings=is_silent_mode,
            ), set_non_mlflow_warnings_behavior_for_current_thread(
                # non-MLflow warnings emitted during autologging setup / enablement are not
                # actionable for the user, as they are a byproduct of the autologging
                # implementation. Accordingly, they should be rerouted to `logger.warning()`.
                # For reference, see recommended warning and event logging
                # behaviors from https://docs.python.org/3/howto/logging.html#when-to-use-logging
                reroute_warnings=True,
                disable_warnings=is_silent_mode,
            ):

                try:
                    # Pass `autolog()` arguments to `log_autolog_called` in keyword format to enable
                    # event loggers to more easily identify important configuration parameters
                    # (e.g., `disable`) without examining positional arguments. Passing positional
                    # arguments to `log_autolog_called` is deprecated in MLflow > 1.13.1
                    AutologgingEventLogger.get_logger().log_autolog_called(
                        name, (), config_to_store
                    )
                except Exception:
                    pass

                _check_and_log_warning_for_unsupported_integration(name)

                return _autolog(*args, **kwargs)

        wrapped_autolog = _update_wrapper_extended(autolog, _autolog)
        # Set the autologging integration name as a function attribute on the wrapped autologging
        # function, allowing the integration name to be extracted from the function. This is used
        # during the execution of import hooks for `mlflow.autolog()`.
        wrapped_autolog.integration_name = name

        if name in _cross_tested_flavor_to_module_name_and_module_key:
            wrapped_autolog.__doc__ = (
                _gen_autologging_package_version_requirements_doc(name) + wrapped_autolog.__doc__
            )
        return wrapped_autolog

    return wrapper


def get_autologging_config(flavor_name, config_key, default_value=None):
    """
    Returns a desired config value for a specified autologging integration.
    Returns `None` if specified `flavor_name` has no recorded configs.
    If `config_key` is not set on the config object, default value is returned.

    :param flavor_name: An autologging integration flavor name.
    :param config_key: The key for the desired config value.
    :param default_value: The default_value to return
    """
    config = AUTOLOGGING_INTEGRATIONS.get(flavor_name)
    if config is not None:
        return config.get(config_key, default_value)
    else:
        return default_value


def autologging_is_disabled(flavor_name):
    """
    Returns a boolean flag of whether the autologging integration is disabled.

    :param flavor_name: An autologging integration flavor name.
    """
    explicit_disabled = get_autologging_config(flavor_name, "disable", True)
    if explicit_disabled:
        return True

    if (
        flavor_name in _cross_tested_flavor_to_module_name_and_module_key
        and not _is_autologging_integration_supported(flavor_name)
    ):
        return get_autologging_config(flavor_name, "disable_for_unsupported_versions", False)

    return False


def _is_testing():
    """
    Indicates whether or not autologging functionality is running in test mode (as determined
    by the `MLFLOW_AUTOLOGGING_TESTING` environment variable). Test mode performs additional
    validation during autologging, including:

        - Checks for the exception safety of arguments passed to model training functions
          (i.e. all additional arguments should be "exception safe" functions or classes)
        - Disables exception handling for patched function logic, ensuring that patch code
          executes without errors during testing
    """
    return os.environ.get(_AUTOLOGGING_TEST_MODE_ENV_VAR, "false") == "true"


# Function attribute used for testing purposes to verify that a given function
# has been wrapped with the `exception_safe_function` decorator
_ATTRIBUTE_EXCEPTION_SAFE = "exception_safe"


def exception_safe_function(function):
    """
    Wraps the specified function with broad exception handling to guard
    against unexpected errors during autologging.
    """
    if _is_testing():
        setattr(function, _ATTRIBUTE_EXCEPTION_SAFE, True)

    def safe_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            if _is_testing():
                raise
            else:
                _logger.warning("Encountered unexpected error during autologging: %s", e)

    safe_function = _update_wrapper_extended(safe_function, function)
    return safe_function


def _exception_safe_class_factory(base_class):
    """
    Creates an exception safe metaclass that inherits from `base_class`.
    """

    class _ExceptionSafeClass(base_class):
        """
        Metaclass that wraps all functions defined on the specified class with broad error handling
        logic to guard against unexpected errors during autlogging.

        Rationale: Patched autologging functions commonly pass additional class instances as
        arguments to their underlying original training routines; for example, Keras autologging
        constructs a subclass of `keras.callbacks.Callback` and forwards it to `Model.fit()`.
        To prevent errors encountered during method execution within such classes from disrupting
        model training, this metaclass wraps all class functions in a broad try / catch statement.

        Note: `ExceptionSafeClass` does not handle exceptions in class methods or static methods,
        as these are not always Python callables and are difficult to wrap
        """

        def __new__(cls, name, bases, dct):
            for m in dct:
                # class methods or static methods are not callable.
                if callable(dct[m]):
                    dct[m] = exception_safe_function(dct[m])
            return base_class.__new__(cls, name, bases, dct)

    return _ExceptionSafeClass


ExceptionSafeClass = _exception_safe_class_factory(type)

# `ExceptionSafeClass` causes an error when used with an abstract class.
#
# ```
# class AbstractClass(abc.ABC):
#    ...
#
# class DerivedClass(AbstractClass, metaclass=ExceptionSafeClass):
#    ...
# ```
#
# This raises:
#
# ```
# TypeError: metaclass conflict: the metaclass of a derived class must be
#            a (non-strict) subclass of the metaclasses of all its bases.
# ```
#
# To avoid this error, create `ExceptionSafeAbstractClass` that is based on `abc.ABCMeta`.
ExceptionSafeAbstractClass = _exception_safe_class_factory(abc.ABCMeta)


class PatchFunction:
    """
    Base class representing a function patch implementation with a callback for error handling.
    `PatchFunction` should be subclassed and used in conjunction with `safe_patch` to
    safely modify the implementation of a function. Subclasses of `PatchFunction` should
    use `_patch_implementation` to define modified ("patched") function implementations and
    `_on_exception` to define cleanup logic when `_patch_implementation` terminates due
    to an unhandled exception.
    """

    @abstractmethod
    def _patch_implementation(self, original, *args, **kwargs):
        """
        Invokes the patch function code.

        :param original: The original, underlying function over which the `PatchFunction`
                         is being applied.
        :param *args: The positional arguments passed to the original function.
        :param **kwargs: The keyword arguments passed to the original function.
        """
        pass

    @abstractmethod
    def _on_exception(self, exception):
        """
        Called when an unhandled standard Python exception (i.e. an exception inheriting from
        `Exception`) or a `KeyboardInterrupt` prematurely terminates the execution of
        `_patch_implementation`.

        :param exception: The unhandled exception thrown by `_patch_implementation`.
        """
        pass

    @classmethod
    def call(cls, original, *args, **kwargs):
        return cls().__call__(original, *args, **kwargs)

    def __call__(self, original, *args, **kwargs):
        try:
            return self._patch_implementation(original, *args, **kwargs)
        except (Exception, KeyboardInterrupt) as e:
            try:
                self._on_exception(e)
            finally:
                # Regardless of what happens during the `_on_exception` callback, reraise
                # the original implementation exception once the callback completes
                raise e


# Represents an active autologging session using two fields:
# - integration: the name of the autologging integration corresponding to the session
# - id: a unique session identifier (e.g., a UUID)
AutologgingSession = namedtuple("AutologgingSession", ["integration", "id"])


class _AutologgingSessionManager:
    _session = None

    @classmethod
    @contextmanager
    def start_session(cls, integration):
        try:
            prev_session = cls._session
            if prev_session is None:
                session_id = uuid.uuid4().hex
                cls._session = AutologgingSession(integration, session_id)
            yield cls._session
        finally:
            # Only end the session upon termination of the context if we created
            # the session; otherwise, leave the session open for later termination
            # by its creator
            if prev_session is None:
                cls._end_session()

    @classmethod
    def active_session(cls):
        return cls._session

    @classmethod
    def _end_session(cls):
        cls._session = None


class AutologgingEventLogger:
    """
    Provides instrumentation hooks for important autologging lifecycle events, including:

        - Calls to `mlflow.autolog()` APIs
        - Calls to patched APIs with associated termination states
          ("success" and "failure due to error")
        - Calls to original / underlying APIs made by patched function code with
          associated termination states ("success" and "failure due to error")

    Default implementations are included for each of these hooks, which emit corresponding
    DEBUG-level logging statements. Developers can provide their own hook implementations
    by subclassing `AutologgingEventLogger` and calling the static
    `AutologgingEventLogger.set_logger()` method to supply a new event logger instance.

    Callers fetch the configured logger via `AutologgingEventLogger.get_logger()`
    and invoke one or more hooks (e.g., `AutologgingEventLogger.get_logger().log_autolog_called()`).
    """

    _event_logger = None

    @staticmethod
    def get_logger():
        """
        Fetches the configured `AutologgingEventLogger` instance for logging.

        :return: The instance of `AutologgingEventLogger` specified via `set_logger`
                 (if configured) or the default implementation of `AutologgingEventLogger`
                 (if a logger was not configured via `set_logger`).
        """
        return AutologgingEventLogger._event_logger or AutologgingEventLogger()

    @staticmethod
    def set_logger(logger):
        """
        Configures the `AutologgingEventLogger` instance for logging. This instance
        is exposed via `AutologgingEventLogger.get_logger()` and callers use it to invoke
        logging hooks (e.g., AutologgingEventLogger.get_logger().log_autolog_called()).

        :param logger: The instance of `AutologgingEventLogger` to use when invoking logging hooks.
        """
        AutologgingEventLogger._event_logger = logger

    def log_autolog_called(self, integration, call_args, call_kwargs):
        """
        Called when the `autolog()` method for an autologging integration
        is invoked (e.g., when a user invokes `mlflow.sklearn.autolog()`)

        :param integration: The autologging integration for which `autolog()` was called.
        :param call_args: **DEPRECATED** The positional arguments passed to the `autolog()` call.
                          This field is empty in MLflow > 1.13.1; all arguments are passed in
                          keyword form via `call_kwargs`.
        :param call_kwargs: The arguments passed to the `autolog()` call in keyword form.
                            Any positional arguments should also be converted to keyword form
                            and passed via `call_kwargs`.
        """
        if len(call_args) > 0:
            warnings.warn(
                "Received %d positional arguments via `call_args`. `call_args` is"
                " deprecated in MLflow > 1.13.1, and all arguments should be passed"
                " in keyword form via `call_kwargs`." % len(call_args),
                category=DeprecationWarning,
                stacklevel=2,
            )
        _logger.debug(
            "Called autolog() method for %s autologging with args '%s' and kwargs '%s'",
            integration,
            call_args,
            call_kwargs,
        )

    def log_patch_function_start(self, session, patch_obj, function_name, call_args, call_kwargs):
        """
        Called upon invocation of a patched API associated with an autologging integration
        (e.g., `sklearn.linear_model.LogisticRegression.fit()`).

        :param session: The `AutologgingSession` associated with the patched API call.
        :param patch_obj: The object (class, module, etc) on which the patched API was called.
        :param function_name: The name of the patched API that was called.
        :param call_args: The positional arguments passed to the patched API call.
        :param call_kwargs: The keyword arguments passed to the patched API call.
        """
        _logger.debug(
            "Invoked patched API '%s.%s' for %s autologging with args '%s' and kwargs '%s'",
            patch_obj,
            function_name,
            session.integration,
            call_args,
            call_kwargs,
        )

    def log_patch_function_success(self, session, patch_obj, function_name, call_args, call_kwargs):
        """
        Called upon successful termination of a patched API associated with an autologging
        integration (e.g., `sklearn.linear_model.LogisticRegression.fit()`).

        :param session: The `AutologgingSession` associated with the patched API call.
        :param patch_obj: The object (class, module, etc) on which the patched API was called.
        :param function_name: The name of the patched API that was called.
        :param call_args: The positional arguments passed to the patched API call.
        :param call_kwargs: The keyword arguments passed to the patched API call.
        """
        _logger.debug(
            "Patched API call '%s.%s' for %s autologging completed successfully. Patched ML"
            " API was called with args '%s' and kwargs '%s'",
            patch_obj,
            function_name,
            session.integration,
            call_args,
            call_kwargs,
        )

    def log_patch_function_error(
        self, session, patch_obj, function_name, call_args, call_kwargs, exception
    ):
        """
        Called when execution of a patched API associated with an autologging integration
        (e.g., `sklearn.linear_model.LogisticRegression.fit()`) terminates with an exception.

        :param session: The `AutologgingSession` associated with the patched API call.
        :param patch_obj: The object (class, module, etc) on which the patched API was called.
        :param function_name: The name of the patched API that was called.
        :param call_args: The positional arguments passed to the patched API call.
        :param call_kwargs: The keyword arguments passed to the patched API call.
        :param exception: The exception that caused the patched API call to terminate.
        """
        _logger.debug(
            "Patched API call '%s.%s' for %s autologging threw exception. Patched API was"
            " called with args '%s' and kwargs '%s'. Exception: %s",
            patch_obj,
            function_name,
            session.integration,
            call_args,
            call_kwargs,
            exception,
        )

    def log_original_function_start(
        self, session, patch_obj, function_name, call_args, call_kwargs
    ):
        """
        Called during the execution of a patched API associated with an autologging integration
        when the original / underlying API is invoked. For example, this is called when
        a patched implementation of `sklearn.linear_model.LogisticRegression.fit()` invokes
        the original implementation of `sklearn.linear_model.LogisticRegression.fit()`.

        :param session: The `AutologgingSession` associated with the patched API call.
        :param patch_obj: The object (class, module, etc) on which the original API was called.
        :param function_name: The name of the original API that was called.
        :param call_args: The positional arguments passed to the original API call.
        :param call_kwargs: The keyword arguments passed to the original API call.
        """
        _logger.debug(
            "Original function invoked during execution of patched API '%s.%s' for %s"
            " autologging. Original function was invoked with args '%s' and kwargs '%s'",
            patch_obj,
            function_name,
            session.integration,
            call_args,
            call_kwargs,
        )

    def log_original_function_success(
        self, session, patch_obj, function_name, call_args, call_kwargs
    ):
        """
        Called during the execution of a patched API associated with an autologging integration
        when the original / underlying API invocation terminates successfully. For example,
        when a patched implementation of `sklearn.linear_model.LogisticRegression.fit()` invokes the
        original / underlying implementation of `LogisticRegression.fit()`, then this function is
        called if the original / underlying implementation successfully completes.

        :param session: The `AutologgingSession` associated with the patched API call.
        :param patch_obj: The object (class, module, etc) on which the original API was called.
        :param function_name: The name of the original API that was called.
        :param call_args: The positional arguments passed to the original API call.
        :param call_kwargs: The keyword arguments passed to the original API call.
        """
        _logger.debug(
            "Original function invocation completed successfully during execution of patched API"
            " call '%s.%s' for %s autologging. Original function was invoked with with"
            " args '%s' and kwargs '%s'",
            patch_obj,
            function_name,
            session.integration,
            call_args,
            call_kwargs,
        )

    def log_original_function_error(
        self, session, patch_obj, function_name, call_args, call_kwargs, exception
    ):
        """
        Called during the execution of a patched API associated with an autologging integration
        when the original / underlying API invocation terminates with an error. For example,
        when a patched implementation of `sklearn.linear_model.LogisticRegression.fit()` invokes the
        original / underlying implementation of `LogisticRegression.fit()`, then this function is
        called if the original / underlying implementation terminates with an exception.

        :param session: The `AutologgingSession` associated with the patched API call.
        :param patch_obj: The object (class, module, etc) on which the original API was called.
        :param function_name: The name of the original API that was called.
        :param call_args: The positional arguments passed to the original API call.
        :param call_kwargs: The keyword arguments passed to the original API call.
        :param exception: The exception that caused the original API call to terminate.
        """
        _logger.debug(
            "Original function invocation threw exception during execution of patched"
            " API call '%s.%s' for %s autologging. Original function was invoked with"
            " args '%s' and kwargs '%s'. Exception: %s",
            patch_obj,
            function_name,
            session.integration,
            call_args,
            call_kwargs,
            exception,
        )


def with_managed_run(autologging_integration, patch_function, tags=None):
    """
    Given a `patch_function`, returns an `augmented_patch_function` that wraps the execution of
    `patch_function` with an active MLflow run. The following properties apply:

        - An MLflow run is only created if there is no active run present when the
          patch function is executed

        - If an active run is created by the `augmented_patch_function`, it is terminated
          with the `FINISHED` state at the end of function execution

        - If an active run is created by the `augmented_patch_function`, it is terminated
          with the `FAILED` if an unhandled exception is thrown during function execution

    Note that, if nested runs or non-fluent runs are created by `patch_function`, `patch_function`
    is responsible for terminating them by the time it terminates (or in the event of an exception).

    :param autologging_integration: The autologging integration associated
                                    with the `patch_function`.
    :param patch_function: A `PatchFunction` class definition or a function object
                           compatible with `safe_patch`.
    :param tags: A dictionary of string tags to set on each managed run created during the
                 execution of `patch_function`.
    """

    def create_managed_run():
        managed_run = mlflow.start_run()
        if tags:
            try_mlflow_log(mlflow.set_tags, tags)
        _logger.info(
            "Created MLflow autologging run with ID '%s', which will track hyperparameters,"
            " performance metrics, model artifacts, and lineage information for the"
            " current %s workflow",
            managed_run.info.run_id,
            autologging_integration,
        )
        return managed_run

    if inspect.isclass(patch_function):

        class PatchWithManagedRun(patch_function):
            def __init__(self):
                super(PatchWithManagedRun, self).__init__()
                self.managed_run = None

            def _patch_implementation(self, original, *args, **kwargs):
                if not mlflow.active_run():
                    self.managed_run = try_mlflow_log(create_managed_run)

                result = super(PatchWithManagedRun, self)._patch_implementation(
                    original, *args, **kwargs
                )

                if self.managed_run:
                    try_mlflow_log(mlflow.end_run, RunStatus.to_string(RunStatus.FINISHED))

                return result

            def _on_exception(self, e):
                if self.managed_run:
                    try_mlflow_log(mlflow.end_run, RunStatus.to_string(RunStatus.FAILED))
                super(PatchWithManagedRun, self)._on_exception(e)

        return PatchWithManagedRun

    else:

        def patch_with_managed_run(original, *args, **kwargs):
            managed_run = None
            if not mlflow.active_run():
                managed_run = try_mlflow_log(create_managed_run)

            try:
                result = patch_function(original, *args, **kwargs)
            except (Exception, KeyboardInterrupt):
                # In addition to standard Python exceptions, handle keyboard interrupts to ensure
                # that runs are terminated if a user prematurely interrupts training execution
                # (e.g. via sigint / ctrl-c)
                if managed_run:
                    try_mlflow_log(mlflow.end_run, RunStatus.to_string(RunStatus.FAILED))
                raise
            else:
                if managed_run:
                    try_mlflow_log(mlflow.end_run, RunStatus.to_string(RunStatus.FINISHED))
                return result

        return patch_with_managed_run


def safe_patch(
    autologging_integration, destination, function_name, patch_function, manage_run=False
):
    """
    Patches the specified `function_name` on the specified `destination` class for autologging
    purposes, preceding its implementation with an error-safe copy of the specified patch
    `patch_function` with the following error handling behavior:

        - Exceptions thrown from the underlying / original function
          (`<destination>.<function_name>`) are propagated to the caller.

        - Exceptions thrown from other parts of the patched implementation (`patch_function`)
          are caught and logged as warnings.


    :param autologging_integration: The name of the autologging integration associated with the
                                    patch.
    :param destination: The Python class on which the patch is being defined.
    :param function_name: The name of the function to patch on the specified `destination` class.
    :param patch_function: The patched function code to apply. This is either a `PatchFunction`
                           class definition or a function object. If it is a function object, the
                           first argument should be reserved for an `original` method argument
                           representing the underlying / original function. Subsequent arguments
                           should be identical to those of the original function being patched.
    :param manage_run: If `True`, applies the `with_managed_run` wrapper to the specified
                       `patch_function`, which automatically creates & terminates an MLflow
                       active run during patch code execution if necessary. If `False`,
                       does not apply the `with_managed_run` wrapper to the specified
                       `patch_function`.
    """
    if manage_run:
        patch_function = with_managed_run(
            autologging_integration,
            patch_function,
            tags={MLFLOW_AUTOLOGGING: autologging_integration},
        )

    patch_is_class = inspect.isclass(patch_function)
    if patch_is_class:
        assert issubclass(patch_function, PatchFunction)
    else:
        assert callable(patch_function)

    def safe_patch_function(*args, **kwargs):
        """
        A safe wrapper around the specified `patch_function` implementation designed to
        handle exceptions thrown during the execution of `patch_function`. This wrapper
        distinguishes exceptions thrown from the underlying / original function
        (`<destination>.<function_name>`) from exceptions thrown from other parts of
        `patch_function`. This distinction is made by passing an augmented version of the
        underlying / original function to `patch_function` that uses nonlocal state to track
        whether or not it has been executed and whether or not it threw an exception.

        Exceptions thrown from the underlying / original function are propagated to the caller,
        while exceptions thrown from other parts of `patch_function` are caught and logged as
        warnings.
        """
        # Reroute warnings encountered during the patch function implementation to an MLflow event
        # logger, and enforce silent mode if applicable (i.e. if the corresponding autologging
        # integration was called with `silent=True`), hiding MLflow event logging statements and
        # hiding all warnings in the autologging preamble and postamble (i.e. the code surrounding
        # the user's original / underlying ML function). Non-MLflow warnings are enabled during the
        # execution of the original / underlying ML function
        #
        # Note that we've opted *not* to apply this context manager as a decorator on
        # `safe_patch_function` because the context-manager-as-decorator pattern uses
        # `contextlib.ContextDecorator`, which creates generator expressions that cannot be pickled
        # during model serialization by ML frameworks such as scikit-learn
        is_silent_mode = get_autologging_config(autologging_integration, "silent", False)
        with set_mlflow_events_and_warnings_behavior_globally(
            # MLflow warnings emitted during autologging training sessions are likely not actionable
            # and result from the autologging implementation invoking another MLflow API.
            # Accordingly, we reroute these warnings to the MLflow event logger with level WARNING
            # For reference, see recommended warning and event logging behaviors from
            # https://docs.python.org/3/howto/logging.html#when-to-use-logging
            reroute_warnings=True,
            disable_event_logs=is_silent_mode,
            disable_warnings=is_silent_mode,
        ), set_non_mlflow_warnings_behavior_for_current_thread(
            # non-MLflow Warnings emitted during the autologging preamble (before the original /
            # underlying ML function is called) and postamble (after the original / underlying ML
            # function is called) are likely not actionable and result from the autologging
            # implementation invoking an API from a dependent library. Accordingly, we reroute these
            # warnings to the MLflow event logger with level WARNING. For reference, see recommended
            # warning and event logging behaviors from
            # https://docs.python.org/3/howto/logging.html#when-to-use-logging
            reroute_warnings=True,
            disable_warnings=is_silent_mode,
        ):

            if _is_testing():
                preexisting_run_for_testing = mlflow.active_run()

            original = gorilla.get_original_attribute(destination, function_name)

            # If the autologging integration associated with this patch is disabled,
            # call the original function and return
            if autologging_is_disabled(autologging_integration):
                return original(*args, **kwargs)

            # Whether or not to exclude auto-autologged content from content explicitly logged via
            # `mlflow.start_run()`
            exclusive = get_autologging_config(autologging_integration, "exclusive", False)

            active_run = mlflow.active_run()

            if active_run and exclusive and not _AutologgingSessionManager.active_session():
                return original(*args, **kwargs)

            # Whether or not the original / underlying function has been called during the
            # execution of patched code
            original_has_been_called = False
            # The value returned by the call to the original / underlying function during
            # the execution of patched code
            original_result = None
            # Whether or not an exception was raised from within the original / underlying function
            # during the execution of patched code
            failed_during_original = False
            # The active MLflow run (if any) associated with patch code execution
            patch_function_run_for_testing = None

            def try_log_autologging_event(log_fn, *args):
                try:
                    log_fn(*args)
                except Exception as e:
                    _logger.debug(
                        "Failed to log autologging event via '%s'. Exception: %s", log_fn, e,
                    )

            with _AutologgingSessionManager.start_session(autologging_integration) as session:
                try:

                    def call_original(*og_args, **og_kwargs):
                        try:
                            try_log_autologging_event(
                                AutologgingEventLogger.get_logger().log_original_function_start,
                                session,
                                destination,
                                function_name,
                                og_args,
                                og_kwargs,
                            )

                            if _is_testing():
                                _validate_args(args, kwargs, og_args, og_kwargs)
                                # By the time `original` is called by the patch implementation, we
                                # assume that either: 1. the patch implementation has already
                                # created an MLflow run or 2. the patch code will not create an
                                # MLflow run during the current execution. Here, we capture a
                                # reference to the active run, which we will use later on to
                                # determine whether or not the patch implementation created
                                # a run and perform validation if necessary
                                nonlocal patch_function_run_for_testing
                                patch_function_run_for_testing = mlflow.active_run()

                            nonlocal original_has_been_called
                            original_has_been_called = True

                            nonlocal original_result
                            # Show all non-MLflow warnings as normal (i.e. not as event logs) during
                            # original function execution, even if silent mode is enabled
                            # (`silent=True`), since these warnings originate from the ML framework
                            # or one of its dependencies and are likely relevant to the caller
                            with set_non_mlflow_warnings_behavior_for_current_thread(
                                disable_warnings=False, reroute_warnings=False,
                            ):
                                original_result = original(*og_args, **og_kwargs)

                            try_log_autologging_event(
                                AutologgingEventLogger.get_logger().log_original_function_success,
                                session,
                                destination,
                                function_name,
                                og_args,
                                og_kwargs,
                            )

                            return original_result
                        except Exception as e:
                            try_log_autologging_event(
                                AutologgingEventLogger.get_logger().log_original_function_error,
                                session,
                                destination,
                                function_name,
                                og_args,
                                og_kwargs,
                                e,
                            )

                            nonlocal failed_during_original
                            failed_during_original = True
                            raise

                    # Apply the name, docstring, and signature of `original` to `call_original`.
                    # This is important because several autologging patch implementations inspect
                    # the signature of the `original` argument during execution
                    call_original = _update_wrapper_extended(call_original, original)

                    try_log_autologging_event(
                        AutologgingEventLogger.get_logger().log_patch_function_start,
                        session,
                        destination,
                        function_name,
                        args,
                        kwargs,
                    )

                    if patch_is_class:
                        patch_function.call(call_original, *args, **kwargs)
                    else:
                        patch_function(call_original, *args, **kwargs)

                    try_log_autologging_event(
                        AutologgingEventLogger.get_logger().log_patch_function_success,
                        session,
                        destination,
                        function_name,
                        args,
                        kwargs,
                    )
                except Exception as e:
                    # Exceptions thrown during execution of the original function should be
                    # propagated to the caller. Additionally, exceptions encountered during test
                    # mode should be reraised to detect bugs in autologging implementations
                    if failed_during_original or _is_testing():
                        raise

                    try_log_autologging_event(
                        AutologgingEventLogger.get_logger().log_patch_function_error,
                        session,
                        destination,
                        function_name,
                        args,
                        kwargs,
                        e,
                    )

                    _logger.warning(
                        "Encountered unexpected error during %s autologging: %s",
                        autologging_integration,
                        e,
                    )

                if _is_testing() and not preexisting_run_for_testing:
                    # If an MLflow run was created during the execution of patch code, verify that
                    # it is no longer active and that it contains expected autologging tags
                    assert not mlflow.active_run(), (
                        "Autologging integration %s leaked an active run" % autologging_integration
                    )
                    if patch_function_run_for_testing:
                        _validate_autologging_run(
                            autologging_integration, patch_function_run_for_testing.info.run_id
                        )

                if original_has_been_called:
                    return original_result
                else:
                    return original(*args, **kwargs)

    _wrap_patch(destination, function_name, safe_patch_function)


def _validate_autologging_run(autologging_integration, run_id):
    """
    For testing purposes, verifies that an MLflow run produced by an `autologging_integration`
    satisfies the following properties:

        - The run has an autologging tag whose value is the name of the autologging integration
        - The run has a terminal status (e.g., KILLED, FAILED, FINISHED)
    """
    client = MlflowClient()
    run = client.get_run(run_id)
    autologging_tag_value = run.data.tags.get(MLFLOW_AUTOLOGGING)
    assert autologging_tag_value == autologging_integration, (
        "Autologging run with id {} failed to set autologging tag with expected value. Expected: "
        "'{}', Actual: '{}'".format(run_id, autologging_integration, autologging_tag_value)
    )
    assert RunStatus.is_terminated(
        RunStatus.from_string(run.info.status)
    ), "Autologging run with id {} has a non-terminal status '{}'".format(run_id, run.info.status)


def _validate_args(
    user_call_args, user_call_kwargs, autologging_call_args, autologging_call_kwargs
):
    """
    Used for testing purposes to verify that, when a patched ML function calls its underlying
    / original ML function, the following properties are satisfied:

        - All arguments supplied to the patched ML function are forwarded to the
          original ML function
        - Any additional arguments supplied to the original function are exception safe (i.e.
          they are either functions decorated with the `@exception_safe_function` decorator
          or classes / instances of classes with type `ExceptionSafeClass`
    """

    def _validate_new_input(inp):
        """
        Validates a new input (arg or kwarg) introduced to the underlying / original ML function
        call during the execution of a patched ML function. The new input is valid if:

            - The new input is a function that has been decorated with `exception_safe_function`
            - OR the new input is a class with the `ExceptionSafeClass` metaclass
            - OR the new input is a list and each of its elements is valid according to the
              these criteria
        """
        if type(inp) == list:
            for item in inp:
                _validate_new_input(item)
        elif callable(inp):
            assert getattr(inp, _ATTRIBUTE_EXCEPTION_SAFE, False), (
                "New function argument '{}' passed to original function is not exception-safe."
                " Please decorate the function with `exception_safe_function`.".format(inp)
            )
        else:
            assert hasattr(inp, "__class__") and type(inp.__class__) in [
                ExceptionSafeClass,
                ExceptionSafeAbstractClass,
            ], (
                "Invalid new input '{}'. New args / kwargs introduced to `original` function "
                "calls by patched code must either be functions decorated with "
                "`exception_safe_function`, instances of classes with the `ExceptionSafeClass` "
                "or `ExceptionSafeAbstractClass` metaclass safe or lists of such exception safe "
                "functions / classes.".format(inp)
            )

    def _validate(autologging_call_input, user_call_input=None):
        """
        Validates that the specified `autologging_call_input` and `user_call_input`
        are compatible. If `user_call_input` is `None`, then `autologging_call_input`
        is regarded as a new input added by autologging and is validated using
        `_validate_new_input`. Otherwise, the following properties must hold:

            - `autologging_call_input` and `user_call_input` must have the same type
              (referred to as "input type")
            - if the input type is a tuple, list or dictionary, then `autologging_call_input` must
              be equivalent to `user_call_input` or be a superset of `user_call_input`
            - for all other input types, `autologging_call_input` and `user_call_input`
              must be equivalent by reference equality or by object equality
        """
        if user_call_input is None and autologging_call_input is not None:
            _validate_new_input(autologging_call_input)
            return

        assert type(autologging_call_input) == type(
            user_call_input
        ), "Type of input to original function '{}' does not match expected type '{}'".format(
            type(autologging_call_input), type(user_call_input)
        )

        if type(autologging_call_input) in [list, tuple]:
            length_difference = len(autologging_call_input) - len(user_call_input)
            assert length_difference >= 0, (
                "{} expected inputs are missing from the call"
                " to the original function.".format(length_difference)
            )
            # If the autologging call input is longer than the user call input, we `zip_longest`
            # will pad the user call input with `None` values to ensure that the subsequent calls
            # to `_validate` identify new inputs added by the autologging call
            for a, u in itertools.zip_longest(autologging_call_input, user_call_input):
                _validate(a, u)
        elif type(autologging_call_input) == dict:
            assert set(user_call_input.keys()).issubset(set(autologging_call_input.keys())), (
                "Keyword or dictionary arguments to original function omit"
                " one or more expected keys: '{}'".format(
                    set(user_call_input.keys()) - set(autologging_call_input.keys())
                )
            )
            for key in autologging_call_input.keys():
                _validate(autologging_call_input[key], user_call_input.get(key, None))
        else:
            assert (
                autologging_call_input is user_call_input
                or autologging_call_input == user_call_input
            ), (
                "Input to original function does not match expected input."
                " Original: '{}'. Expected: '{}'".format(autologging_call_input, user_call_input)
            )

    _validate(autologging_call_args, user_call_args)
    _validate(autologging_call_kwargs, user_call_kwargs)
