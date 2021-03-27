import json
from typing import Any, Dict
from time import sleep

import requests
from requests import PreparedRequest, exceptions as requests_exceptions
from requests.auth import AuthBase
import pendulum

from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook


class FivetranHook(BaseHook):
    """
    Fivetran API interaction hook.

    :param fivetran_conn_id: Maps to the id of the Connection to be used to
        configure this hook.
    :type fivetran_conn_id: str
    :param timeout_seconds: The amount of time in seconds the requests library
        will wait before timing-out.
    :type timeout_seconds: int
    :param retry_limit: The number of times to retry the connection in case of
        service outages.
    :type retry_limit: int
    :param retry_delay: The number of seconds to wait between retries.
    :type retry_delay: float
    """

    conn_name_attr = 'fivetran_conn_id'
    default_conn_name = 'fivetran_default'
    conn_type = 'fivetran'
    hook_name = 'Fivetran'
    api_user_agent = 'airflow_provider_fivetran/0.1'
    api_protocol = 'https'
    api_host = 'api.fivetran.com'
    api_path_connectors = 'v1/connectors/'


    @staticmethod
    def get_connection_form_widgets() -> Dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import PasswordField

        return {
            "extra__fivetran__token": PasswordField(
                lazy_gettext('Token'), widget=BS3PasswordFieldWidget()
            ),
        }

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ['schema', 'port', 'extra'],
            "relabeling": {},
            "placeholders": {
                'host': 'Fivetran API Hostname',
                'login': 'Fivetran API Key',
                'password': 'Fivetran API Secret',
            },
        }

    def __init__(
        self,
        fivetran_conn_id: str = "fivetran",
        timeout_seconds: int = 180,
        retry_limit: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        super().__init__(None) # Passing None fixes a runtime problem in Airflow 1
        self.fivetran_conn = self.get_connection(fivetran_conn_id)
        self.timeout_seconds = timeout_seconds
        if retry_limit < 1:
            raise ValueError("Retry limit must be greater than equal to 1")
        self.retry_limit = retry_limit
        self.retry_delay = retry_delay

    def _do_api_call(self, endpoint_info, json=None):
        """
        Utility function to perform an API call with retries

        :param endpoint_info: Tuple of method and endpoint
        :type endpoint_info: tuple[string, string]
        :param json: Parameters for this API call.
        :type json: dict
        :return: If the api call returns a OK status code,
            this function returns the response in JSON. Otherwise,
            we throw an AirflowException.
        :rtype: dict
        """
        method, endpoint = endpoint_info
        auth = (self.fivetran_conn.login, self.fivetran_conn.password)
        host = self.fivetran_conn.host
        host = host if host is not None and host != "" else self.api_host
        url = f"{self.api_protocol}://{host}/{endpoint}"

        headers = {
            "User-Agent": self.api_user_agent
        }

        if method == "GET":
            request_func = requests.get
        elif method == "POST":
            request_func = requests.post
        elif method == "PATCH":
            request_func = requests.patch
            headers.update({"Content-Type": "application/json;version=2"})
        else:
            raise AirflowException("Unexpected HTTP Method: " + method)

        attempt_num = 1
        while True:
            try:
                response = request_func(
                    url,
                    data=json if method in ("POST", "PATCH") else None,
                    params=json if method in ("GET") else None,
                    auth=auth,
                    headers=headers
                )
                response.raise_for_status()
                self.log.info("requests url: " + str(response.request.url))
                self.log.info("requests body: " + str(response.request.body))
                self.log.info("requests headers: " + str(response.request.headers))
                return response.json()
            except requests_exceptions.RequestException as e:
                if not _retryable_error(e):
                    # In this case, the user probably made a mistake.
                    # Don't retry.
                    raise AirflowException(
                        f"Response: {e.response.content}, "
                        f"Status Code: {e.response.status_code}"
                    )

                self._log_request_error(attempt_num, e)

            if attempt_num == self.retry_limit:
                raise AirflowException(
                    f"API request to Fivetran failed {self.retry_limit} times."
                    " Giving up."
                )

            attempt_num += 1
            sleep(self.retry_delay)

    def _log_request_error(self, attempt_num: int, error: str) -> None:
        self.log.error(
            "Attempt %s API Request to Fivetran failed with reason: %s",
            attempt_num,
            error,
        )

    def _connector_ui_url(self, service_name, schema_name):
        return (
            f"https://fivetran.com/dashboard/connectors/"
            f"{service_name}/{schema_name}"
        )

    def _connector_ui_url_logs(self, service_name, schema_name):
        return self._connector_ui_url(service_name, schema_name) + "/logs"

    def _connector_ui_url_setup(self, service_name, schema_name):
        return self._connector_ui_url(service_name, schema_name) + "/setup"

    def get_connector(self, connector_id):
        """
        Fetches the detail of a connector.

        :param connector_id: Fivetran connector_id, found in connector settings
            page in the Fivetran user interface.
        :type connector_id: str
        :rtype: Dict
        """
        if connector_id == "":
            raise ValueError("No value specified for connector_id")
        endpoint = self.api_path_connectors + connector_id
        resp = self._do_api_call(("GET", endpoint))
        return resp["data"]


    def check_connector(self, connector_id):
        """
        Ensures connector configuration has been completed successfully and is in
            a functional state.

        :param connector_id: Fivetran connector_id, found in connector settings
            page in the Fivetran user interface.
        :type connector_id: str
        """
        connector_details = self.get_connector(connector_id)
        service_name = connector_details["service"]
        schema_name = connector_details["schema"]
        setup_state = connector_details["status"]["setup_state"]
        if setup_state != "connected":
            raise AirflowException(
                f'Fivetran connector "{connector_id}" not correctly configured, '
                f"status: {setup_state}\nPlease see: "
                f"{self._connector_ui_url_setup(service_name, schema_name)}"
            )
        self.log.info(
            f"Connector type: {service_name}, connector schema: {schema_name}"
        )
        self.log.info(
            f"Connectors logs at "
            f"{self._connector_ui_url_logs(service_name, schema_name)}"
        )
        return True

    def set_manual_schedule(self, connector_id):
        """
        Set connector to manual sync mode, required to force sync through the API.
            Syncs will no longer be performed automatically and must be started
            via the API.

        :param connector_id: Fivetran connector_id, found in connector settings
            page in the Fivetran user interface.
        :type connector_id: str
        """
        endpoint = self.api_path_connectors + connector_id
        return self._do_api_call(
            ("PATCH", endpoint),
            json.dumps({"schedule_type": "manual"})
        )

    def start_fivetran_sync(self, connector_id):
        """
        :param connector_id: Fivetran connector_id, found in connector settings
            page in the Fivetran user interface.
        :type connector_id: str
        """
        endpoint = self.api_path_connectors + connector_id + "/force"
        return self._do_api_call(("POST", endpoint))

    def get_last_sync(self, connector_id):
        """
        Get the last time Fivetran connector completed a sync.
            Used with FivetranSensor to monitor sync completion status.

        :param connector_id: Fivetran connector_id, found in connector settings
            page in the Fivetran user interface.
        :type connector_id: str
        """
        connector_details = self.get_connector(connector_id)
        succeeded_at = self._parse_timestamp(connector_details["succeeded_at"])
        failed_at = self._parse_timestamp(connector_details["failed_at"])
        return succeeded_at if succeeded_at > failed_at else failed_at

    def get_sync_status(self, connector_id, previous_completed_at):
        """
        For sensor, return True if connector's 'succeeded_at' field has updated.
        :param connector_id: Fivetran connector_id, found in connector settings
            page in the Fivetran user interface.
        :type connector_id: str
        :param previous_completed_at: The last time the connector ran, collected on Sensor
            initialization.
        :type previous_completed_at: pendulum.datetime.DateTime
        """
        # @todo Need logic here to tell if the sync is not running at all and not
        # likely to run in the near future.
        connector_details = self.get_connector(connector_id)
        succeeded_at = self._parse_timestamp(connector_details["succeeded_at"])
        failed_at = self._parse_timestamp(connector_details["failed_at"])
        current_completed_at = (
            succeeded_at if succeeded_at > failed_at else failed_at
        )

        # The only way to tell if a sync failed is to check if its latest
        # failed_at value is greater than then last known "sync completed at" value.
        if failed_at > previous_completed_at:
            service_name = connector_details["service"]
            schema_name = connector_details["schema"]
            raise AirflowException(
                f'Fivetran sync for connector "{connector_id}" failed; '
                f"please see logs at "
                f"{self._connector_ui_url_logs(service_name, schema_name)}"
            )

        sync_state = connector_details["status"]["sync_state"]
        self.log.info(f'Connector "{connector_id}": sync_state = {sync_state}')

        # Check if sync started by FivetranOperator has finished
        # indicated by new 'succeeded_at' timestamp
        if current_completed_at > previous_completed_at:
            self.log.info('Connector "{}": succeeded_at: {}'.format(
                connector_id, succeeded_at.to_iso8601_string())
            )
            return True
        else:
            return False

    def _parse_timestamp(self, api_time):
        """
        Returns either the pendulum-parsed actual timestamp or
            a very out-of-date timestamp if not set

        :param api_time: timestamp format as returned by the Fivetran API.
        :type api_time: str
        :rtype: Pendulum.DateTime
        """
        return (
            pendulum.parse(api_time)
            if api_time is not None
            else pendulum.from_timestamp(-1)
        )


def _retryable_error(exception) -> bool:
    return (
        isinstance(
            exception,
            (requests_exceptions.ConnectionError, requests_exceptions.Timeout),
        )
        or exception.response is not None
        and exception.response.status_code >= 500
    )


class _TokenAuth(AuthBase):
    """
    Helper class for requests Auth field. AuthBase requires you to implement the
        __call__ magic function.
    """

    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        r.headers["Authorization"] = "Bearer " + self.token
        return r
