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
import os
from os import PathLike
from typing import List, Optional, Union, cast

from requests import Session
from rtt_sdk import models
from rtt_sdk.__version__ import __title__, __version__
from rtt_sdk.client import RTTClient


class SlingshotClient(RTTClient):
    def __init__(
        self,
        url: Optional[str] = os.environ.get("RTT_PLATFORM_SERVER", None),
        token: Optional[str] = os.environ.get("RTT_PLATFORM_TOKEN", None),
        instance: Optional[str] = cast(models.Tool, os.environ.get("RTT_PLATFORM_INSTANCE", None)),
        loop: Optional[asyncio.AbstractEventLoop] = None,
        debug: bool = False,
        interactive: bool = True,
        session: Optional[Session] = None,
        ssl_verify: bool = True,
        user_agent: str = f"{__title__}/{__version__}",
    ):
        super().__init__(
            tool=models.Tool.slingshot,
            url=url,
            token=token,
            instance=instance,
            loop=loop,
            debug=debug,
            interactive=interactive,
            session=session,
            ssl_verify=ssl_verify,
            user_agent=user_agent,
        )

    async def camera_capture_raw(
        self,
        camera_id: int,
        quality: Optional[int] = None,
        *,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> models.CameraCaptureResults:
        arguments = models.CameraCaptureArguments(camera_id, quality)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.CameraCaptureResults(**task.results.dict())

    async def camera_capture(
        self,
        camera_id: int,
        quality: Optional[int] = None,
        *,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> bytes:
        raise NotImplementedError

    async def camera_list(
        self, instance: Optional[Union[models.InstanceInResponse, str]] = None
    ) -> List[models.Camera]:
        arguments = models.CameraListArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.CameraListResults(**task.results.dict()).cameras or []

    async def context_idle(self, *, instance: Optional[Union[models.InstanceInResponse, str]] = None) -> int:
        arguments = models.ContextIdleArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ContextIdleResults(**task.results.dict())
        if not results.minutes:
            raise KeyError
        return results.minutes

    async def context_process(
        self, *, instance: Optional[Union[models.InstanceInResponse, str]] = None
    ) -> models.ContextProcessResults:
        arguments = models.ContextProcessArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.ContextProcessResults(**task.results.dict())

    async def context_user(
        self, verbose: bool, *, instance: Optional[Union[models.InstanceInResponse, str]] = None
    ) -> models.ContextUserResults:
        arguments = models.ContextUserArguments(verbose=verbose)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.ContextUserResults(**task.results.dict())

    async def exit(self, *, instance: Optional[Union[models.InstanceInResponse, str]] = None) -> None:
        arguments = models.ExitArguments()
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_change_directory(
        self, directory: Optional[str] = None, *, instance: Optional[Union[models.InstanceInResponse, str]] = None
    ) -> str:
        arguments = models.FileChangeDirectoryArguments(directory)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.FileChangeDirectoryResults(**task.results.dict())
        if not results.directory:
            raise KeyError
        return results.directory

    async def file_copy(
        self,
        source: str,
        destination: str,
        force: Optional[bool] = None,
        *,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> None:
        arguments = models.FileCopyArguments(source=source, destination=destination, force=force)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_download_raw(
        self, path: str, *, instance: Optional[Union[models.InstanceInResponse, str]] = None
    ) -> models.FileDownloadResults:
        arguments = models.FileDownloadArguments(path=path)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.FileDownloadResults(**task.results.dict())

    async def file_download(
        self, path: str, *, instance: Optional[Union[models.InstanceInResponse, str]] = None
    ) -> bytes:
        raise NotImplementedError

    async def file_list(
        self,
        directory: str,
        *,
        time_format: Optional[models.TimeFormat] = None,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> List[models.FileOrDirectory]:
        arguments = models.FileListArguments(directory=directory, time_format=time_format)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.FileListResults(**task.results.dict()).entries or []

    async def file_make_directory(
        self, path: str, *, instance: Optional[Union[models.InstanceInResponse, str]] = None
    ) -> None:
        arguments = models.FileMakeDirectoryArguments(path=path)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_move(
        self,
        source: str,
        destination: str,
        *,
        force: Optional[bool] = None,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> None:
        arguments = models.FileMoveArguments(source=source, destination=destination, force=force)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_remove(
        self,
        path: str,
        *,
        force: Optional[bool] = None,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> None:
        arguments = models.FileRemoveArguments(path=path, force=force)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_upload_raw(
        self,
        path: str,
        data: models.BlobReferenceOrData,
        *,
        force: Optional[bool] = None,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> None:
        arguments = models.FileUploadArguments(data=data, path=path, force=force)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_upload(
        self,
        path: str,
        data: Union[bytes, PathLike, str],
        *,
        force: Optional[bool] = None,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> None:
        raise NotImplementedError

    async def host_file_raw(
        self,
        endpoint: str,
        data: models.BlobReferenceOrData,
        *,
        base_url: Optional[str] = None,
        encoding: Optional[models.HostingEncoding] = None,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> str:
        arguments = models.HostFileArguments(data=data, base_url=base_url, endpoint=endpoint, encoding=encoding)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.HostFileResults(**task.results.dict())
        if not results.url:
            raise KeyError
        return results.url

    async def host_file(
        self,
        endpoint: str,
        data: Union[bytes, PathLike, str],
        *,
        base_url: Optional[str] = None,
        encoding: Optional[models.HostingEncoding] = None,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> None:
        raise NotImplementedError

    async def host_shellcode(
        self,
        endpoint: str,
        data: Union[bytes, PathLike, str],
        *,
        base_url: Optional[str] = None,
        encoding: Optional[models.HostingEncoding] = None,
        instance: Optional[Union[models.InstanceInResponse, str]] = None,
    ) -> None:
        raise NotImplementedError
