import concurrent.futures
import logging
import sys
import threading
import uuid

from py4j.java_gateway import CallbackServerParameters

from pyspark import SparkContext

import mlflow
from mlflow.exceptions import MlflowException
from mlflow.tracking.client import MlflowClient
from mlflow.tracking.context.abstract_context import RunContextProvider
from mlflow.utils.autologging_utils import (
    autologging_is_disabled,
    ExceptionSafeClass,
)
from mlflow.spark import FLAVOR_NAME

_JAVA_PACKAGE = "org.mlflow.spark.autologging"
_SPARK_TABLE_INFO_TAG_NAME = "sparkDatasourceInfo"

_logger = logging.getLogger(__name__)
_lock = threading.Lock()
_table_infos = []
_spark_table_info_listener = None

# Queue & singleton consumer thread for logging Spark datasource info asynchronously
_metric_queue = []
_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


# Exposed for testing
def _get_current_listener():
    global _spark_table_info_listener
    return _spark_table_info_listener


def _get_table_info_string(path, version, data_format):
    if data_format == "delta":
        return "path={path},version={version},format={format}".format(
            path=path, version=version, format=data_format
        )
    return "path={path},format={format}".format(path=path, format=data_format)


def _merge_tag_lines(existing_tag, new_table_info):
    if existing_tag is None:
        return new_table_info
    if new_table_info in existing_tag:
        return existing_tag
    return "\n".join([existing_tag, new_table_info])


def add_table_info_to_context_provider(path, version, data_format):
    with _lock:
        _table_infos.append((path, version, data_format))


def _get_spark_major_version(sc):
    spark_version_parts = sc.version.split(".")
    spark_major_version = None
    if len(spark_version_parts) > 0:
        spark_major_version = int(spark_version_parts[0])
    return spark_major_version


def _get_jvm_event_publisher():
    """
    Get JVM-side object implementing the following methods:
    - init() for initializing JVM state needed for autologging (e.g. attaching a SparkListener
      to watch for datasource reads)
    - register(subscriber) for registering subscribers to receive datasource events
    """
    jvm = SparkContext._gateway.jvm
    qualified_classname = "{}.{}".format(_JAVA_PACKAGE, "MlflowAutologEventPublisher")
    return getattr(jvm, qualified_classname)


def _set_run_tag_async(run_id, path, version, data_format):
    _thread_pool.submit(
        _set_run_tag, run_id=run_id, path=path, version=version, data_format=data_format
    )


def _set_run_tag(run_id, path, version, data_format):
    client = MlflowClient()
    table_info_string = _get_table_info_string(path, version, data_format)
    existing_run = client.get_run(run_id)
    existing_tag = existing_run.data.tags.get(_SPARK_TABLE_INFO_TAG_NAME)
    new_table_info = _merge_tag_lines(existing_tag, table_info_string)
    client.set_tag(run_id, _SPARK_TABLE_INFO_TAG_NAME, new_table_info)


def _listen_for_spark_activity(spark_context):
    global _spark_table_info_listener
    if _get_current_listener() is not None:
        return

    if _get_spark_major_version(spark_context) < 3:
        raise MlflowException("Spark autologging unsupported for Spark versions < 3")

    gw = spark_context._gateway
    params = gw.callback_server_parameters
    callback_server_params = CallbackServerParameters(
        address=params.address,
        port=params.port,
        daemonize=True,
        daemonize_connections=True,
        eager_load=params.eager_load,
        ssl_context=params.ssl_context,
        accept_timeout=params.accept_timeout,
        read_timeout=params.read_timeout,
        auth_token=params.auth_token,
    )
    callback_server_started = gw.start_callback_server(callback_server_params)

    try:
        event_publisher = _get_jvm_event_publisher()
        event_publisher.init(1)
        _spark_table_info_listener = PythonSubscriber()
        event_publisher.register(_spark_table_info_listener)
    except Exception as e:
        if callback_server_started:
            try:
                gw.shutdown_callback_server()
            except Exception as e:
                _logger.warning(
                    "Failed to shut down Spark callback server for autologging: %s", str(e)
                )
        _spark_table_info_listener = None
        raise MlflowException(
            "Exception while attempting to initialize JVM-side state for "
            "Spark datasource autologging. Please create a new Spark session "
            "and ensure you have the mlflow-spark JAR attached to your Spark "
            "session as described in "
            "http://mlflow.org/docs/latest/tracking.html#"
            "automatic-logging-from-spark-experimental. "
            "Exception:\n%s" % e
        )

    # Register context provider for Spark autologging
    from mlflow.tracking.context.registry import _run_context_provider_registry

    _run_context_provider_registry.register(SparkAutologgingContext)

    _logger.info("Autologging successfully enabled for spark.")


def _get_repl_id():
    """
    Get a unique REPL ID for a PythonSubscriber instance. This is used to distinguish between
    REPLs in multitenant, REPL-aware environments where multiple Python processes may share the
    same Spark JVM (e.g. in Databricks). In such environments, we pull the REPL ID from Spark
    local properties, and expect that the PythonSubscriber for the current Python process only
    receives events for datasource reads triggered by the current process.
    """
    repl_id = SparkContext.getOrCreate().getLocalProperty("spark.databricks.replId")
    if repl_id:
        return repl_id
    main_file = sys.argv[0] if len(sys.argv) > 0 else "<console>"
    return "PythonSubscriber[{filename}][{id}]".format(filename=main_file, id=uuid.uuid4().hex)


class PythonSubscriber(object, metaclass=ExceptionSafeClass):
    """
    Subscriber, intended to be instantiated once per Python process, that logs Spark table
    information propagated from Java to the current MLflow run, starting a run if necessary.
    class implements a Java interface (org.mlflow.spark.autologging.MlflowAutologEventSubscriber,
    defined in the mlflow-spark package) that's called-into by autologging logic in the JVM in order
    to propagate Spark datasource read events to Python.

    This class leverages the Py4j callback mechanism to receive callbacks from the JVM, see
    https://www.py4j.org/advanced_topics.html#implementing-java-interfaces-from-python-callback for
    more information.
    """

    def __init__(self):
        self._repl_id = _get_repl_id()

    def toString(self):
        # For debugging
        return "PythonSubscriber<replId=%s>" % self.replId()

    def ping(self):
        return None

    def notify(self, path, version, data_format):
        try:
            self._notify(path, version, data_format)
        except Exception as e:
            _logger.error(
                "Unexpected exception %s while attempting to log Spark datasource "
                "info. Exception:\n",
                e,
            )

    def _notify(self, path, version, data_format):
        """
        Method called by Scala SparkListener to propagate datasource read events to the current
        Python process
        """
        if autologging_is_disabled(FLAVOR_NAME):
            return
        # If there's an active run, simply set the tag on it
        # Note that there's a TOCTOU race condition here - active_run() here can actually throw
        # if the main thread happens to end the run & pop from the active run stack after we check
        # the stack size but before we peek
        active_run = mlflow.active_run()
        if active_run:
            _set_run_tag_async(active_run.info.run_id, path, version, data_format)
        else:
            add_table_info_to_context_provider(path, version, data_format)

    def replId(self):
        return self._repl_id

    class Java:
        implements = ["{}.MlflowAutologEventSubscriber".format(_JAVA_PACKAGE)]


class SparkAutologgingContext(RunContextProvider):
    """
    Context provider used when there's no active run. Accumulates datasource read information,
    then logs that information to the next-created run & clears the accumulated information.
    """

    def in_context(self):
        return True

    def tags(self):
        # if autologging is disabled, then short circuit `tags()` and return empty dict.
        if autologging_is_disabled(FLAVOR_NAME):
            return {}
        with _lock:
            global _table_infos
            seen = set()
            unique_infos = []
            for info in _table_infos:
                if info not in seen:
                    unique_infos.append(info)
                    seen.add(info)
            if len(unique_infos) > 0:
                tags = {
                    _SPARK_TABLE_INFO_TAG_NAME: "\n".join(
                        [_get_table_info_string(*info) for info in unique_infos]
                    )
                }
            else:
                tags = {}
            return tags
