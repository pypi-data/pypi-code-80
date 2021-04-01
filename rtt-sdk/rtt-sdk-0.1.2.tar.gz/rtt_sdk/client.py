# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NetSPI <rtt.support@netspi.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import json
import os
import sys
import time
import webbrowser
from typing import Any, Dict, List, Optional, Union, cast

from requests import Response, Session

from rtt_sdk import exceptions, logging
from rtt_sdk.__version__ import __compatible_schema_version__, __title__, __version__
from rtt_sdk.helpers import get_current_file_name, is_task_failed, is_task_finished
from rtt_sdk.models import InstanceInResponse, ScriptArguments, TaskContext, TaskDetails, Tool
from rtt_sdk.openapi import OpenAPI, RequestBody
from rtt_sdk.schema import Schema
from rtt_sdk.stream import WebsocketStream

JSONResponse = Dict[str, Any]
ServerResponse = Union[JSONResponse, bytes]

#
# TODO List:
#
# - Race condition for setting up the websocket vs first task
# - Raise exceptions for tasks with bad statuses (error_info transforms)
# - Expose the feed subscription with callback registrations
# - Add a generic instance/task query APIs
# - Overload RTTClient init in Slingshot client to remove "tool" arg
# - Parameterize the get/post functions more
# - Add docstrings to everything
# - Dynamic class construction for ssclient.context.user
# - Look at alias function names (getuid, etc.)


class RTTClient:
    """
    Represents a RTT platform server client connection.

    Args:
        url: Platform server URL (otherwise from ENV).
        token: Authentication token (otherwise from ENV).
        ssl_verify: SSL certificate verification
    """

    def __init__(
        self,
        url: Optional[str] = os.environ.get("RTT_PLATFORM_SERVER", None),
        token: Optional[str] = os.environ.get("RTT_PLATFORM_TOKEN", None),
        tool: Optional[Tool] = cast(Tool, os.environ.get("RTT_PLATFORM_TOOL", None)),
        instance: Optional[str] = cast(Tool, os.environ.get("RTT_PLATFORM_INSTANCE", None)),
        loop: Optional[asyncio.AbstractEventLoop] = None,
        debug: bool = False,
        interactive: bool = True,
        session: Optional[Session] = None,
        ssl_verify: bool = True,
        user_agent: str = f"{__title__}/{__version__}",
    ):
        if not url:
            raise ValueError("url is a required parameter")
        if not tool:
            raise ValueError("tool is a required parameter")

        if not loop:
            loop = asyncio.get_running_loop()

        self._debug = debug
        self._tool = tool
        self._instance = instance
        self._url = url.rstrip("/")
        self._api_url = f"{self._url}/api"
        self._session = session or Session()
        self._session.verify = ssl_verify
        self._task_events: Dict[str, asyncio.Event] = {}
        self._task_store: Dict[str, TaskDetails] = {}

        try:
            schema_text = self._session.get(f"{self._url}/openapi.json").text
            self._schema: OpenAPI = OpenAPI(**json.loads(schema_text))
        except Exception as e:
            raise exceptions.RTTServerError from e

        if self._schema.info.version != __compatible_schema_version__:
            raise exceptions.RTTIncompatibleServer(f"{self._schema.info.version} != {__compatible_schema_version__}")

        self._tasks_schema_map = self._parse_schema()

        if not token:
            if interactive:
                token = self.get_token_interactive()
            else:
                raise ValueError("token is a required parameter")

        self._headers = {"User-Agent": user_agent, "Authorization": f"Bearer {token}"}

        self._task_stream = WebsocketStream(self, f"{self._api_url}/{self._tool}/tasks/feed")
        self._task_stream.add_callback(self._task_stream_callback)
        self._task_stream_task = asyncio.create_task(self._task_stream.connect())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def _task_stream_callback(self, data: bytes):
        task = TaskDetails(**json.loads(data))
        task_id = str(task.id)

        if task.command == "Script":
            return

        self._task_store[task_id] = task
        if task_id not in self._task_events:
            self._task_events[task_id] = asyncio.Event()
        if is_task_finished(self._task_store[task_id].delivery):
            self._task_events[task_id].set()

    def _parse_schema(self) -> Dict[str, str]:
        map: Dict[str, str] = {}
        for path, info in self._schema.paths.items():
            if "/tasks/" not in path or not info.post:
                continue
            if not isinstance(info.post.requestBody, RequestBody):
                raise exceptions.RTTParsingError("Server schema is invalid")
            try:
                schema_ref = info.post.requestBody.content["application/json"].schema_.ref
                schema_name = schema_ref.split("/")[-1]
                _ = getattr(sys.modules["rtt_sdk.models"], schema_name)
                map[schema_name] = path
            except Exception as e:
                raise exceptions.RTTParsingError from e
        return map

    def set_instance(self, instance: Union[InstanceInResponse, str]) -> None:
        self._instance = instance.id if isinstance(instance, InstanceInResponse) else instance

    def request(
        self,
        verb: str,
        path: str,
        query_data: Dict = {},
        post_data: Optional[Dict] = None,
        multi_part: Optional[Dict] = None,
        **kwargs,
    ) -> Response:
        """
        Make an HTTP request to the platform server.

        Args:
            verb: The HTTP method to call ('get', 'post', 'put', 'delete')
            path: Path or full URL to query ('/sub' or 'http://server/sub')
            query_data: Data to send as query parameters
            post_data: Data to send in the body (as json)
            multi_part: Multi-part form data (files)
            **kwargs: Extra options for the request
        Returns:
            A requests result object.
        Raises:
            RTTAuthenticationError: When authentication is invalid
            RTTValidationError: When the request structure is invalid
            RTTHttpError: For any other HTTP errors
        """
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = f"{self._api_url}/{path.lstrip('/')}"
            url = url.replace("/api/api/", "/api/")  # TODO: I know...

        if "context" not in query_data:
            query_data["context"] = TaskContext.script

        if "{tool}" in url and self._tool:
            url = url.replace("{tool}", self._tool)

        # TODO: Handle retries
        response = self._session.request(
            verb,
            url,
            headers=getattr(self, "_headers", {}),
            params=query_data,
            json=post_data,
            files=multi_part,
            **kwargs,
        )
        if self._debug:
            logging.debug(f"[{response.status_code}] {url} : {response.content.decode(errors='replace')}")
        if 200 <= response.status_code < 300:
            return response

        error_message: Union[bytes, str] = response.content
        try:
            error_message = response.json()["detail"]
            if isinstance(error_message, list):
                error_message = error_message[0]["msg"]
        except (KeyError, ValueError, TypeError):
            pass

        error_class = exceptions.RTTHttpError
        if response.status_code == 400:
            error_class = exceptions.RTTValidationError
        elif response.status_code == 401:
            error_class = exceptions.RTTAuthenticationError

        raise error_class(
            response_code=response.status_code,
            message=error_message,
            response_body=response.content,
        )

    def _convert_to_json(self, response: Response) -> JSONResponse:
        if response.headers["Content-Type"] == "application/json":
            try:
                return response.json()
            except Exception as e:
                raise exceptions.RTTParsingError(message="Failed to parse the server message") from e
        else:
            raise exceptions.RTTParsingError(
                message=f'Server content type is invalid: {response.headers["Content-Type"]}',
                response_body=response.content,
            )

    def get(self, path: str, *args, **kwargs) -> JSONResponse:
        return self._convert_to_json(self.request("get", path, *args, **kwargs))

    def post(self, path: str, *args, **kwargs) -> JSONResponse:
        return self._convert_to_json(self.request("post", path, *args, **kwargs))

    def put(self, path: str, *args, **kwargs) -> JSONResponse:
        return self._convert_to_json(self.request("put", path, *args, **kwargs))

    def get_token_interactive(self) -> str:
        auth_start = self.get(f"/{self._tool}/scripts/auth/start")
        logging.success(f'Script authentication requested: {auth_start["verifyUrl"]}')
        webbrowser.open(auth_start["verifyUrl"])

        script_arguments = ScriptArguments(name=get_current_file_name())

        max_attempts = 30
        sleep_delay = 2
        while max_attempts > 0:
            max_attempts -= 1
            try:
                auth_finish = self.post(auth_start["finishUrl"], post_data=script_arguments.dict())
                return auth_finish["access_token"]
            except exceptions.RTTHttpError as e:
                if e.response_code not in [401, 403]:
                    raise e
                time.sleep(sleep_delay)
        raise exceptions.RTTAuthenticationTimedOut

    def get_instances(self, tool: Optional[Tool] = None) -> List[InstanceInResponse]:
        tool = tool if tool else self._tool
        return [InstanceInResponse(**i) for i in cast(List[Any], self.get(f"/{tool}/instances"))]

    def create_task(self, arguments: Schema, instance: Optional[Union[InstanceInResponse, str]] = None) -> TaskDetails:
        schema_name = arguments.__class__.__name__
        if schema_name not in self._tasks_schema_map.keys():
            raise ValueError(f"Schema object for create_task is invalid: {arguments}")
        endpoint = self._tasks_schema_map[schema_name]
        if "{instance}" in endpoint:
            if instance:
                instance_id = instance.id if isinstance(instance, InstanceInResponse) else instance
            elif self._instance:
                instance_id = self._instance
            else:
                raise ValueError("Cannot create tasking without specifying a target instance")
            endpoint = endpoint.replace("{instance}", str(instance_id))
        task = TaskDetails(**self.post(endpoint, post_data=arguments.dict()))
        return task

    async def create_task_and_wait(
        self, arguments: Schema, instance: Optional[Union[InstanceInResponse, str]] = None
    ) -> TaskDetails:
        task = self.create_task(arguments, instance=instance)
        task_id = str(task.id)

        if not self._task_stream.cursor:
            self._task_stream.cursor = task_id

        if task_id not in self._task_events:
            self._task_events[task_id] = asyncio.Event()

        await self._task_events[task_id].wait()
        task = self._task_store[task_id]

        if is_task_failed(task.status):
            if task.results.error_info:
                raise exceptions.RTTTaskError(task.results.error_info)
            else:
                raise exceptions.RTTError("A task failed, but no error information was returned")
        return task
