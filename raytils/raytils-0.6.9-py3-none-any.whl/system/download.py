# -*- coding: utf-8 -*-
import io
import random
import shutil
import sys
import uuid
from multiprocessing.pool import ThreadPool
import pathlib

import requests
from PIL import Image
import time
from urllib.parse import urlparse

from tqdm import tqdm

from raytils.system import available_cpu_count


class Downloader:
    """Arbitrary file downloader from URLS .get_all returns old_url to local file.

    Example:
        To get all images from a server

        >>> dl = Downloader(["https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba"])
        >>> images = dl.get_all()  # to poll for all
        >>> for url, local_file in dl.get():
        >>>     print(f"Downloaded {local_file} from {url}")  # to iterate over (lazy dl)

    """
    def __init__(self, urls):
        self._urls = urls
        self._progress_bar = tqdm(total=len(self._urls))
        self.save_directory = pathlib.Path(f"/tmp/raytils/system/downloader/{uuid.uuid4()}")

    def _create_temp_file(self, like_url):
        try:
            name = pathlib.Path(urlparse(url=like_url).path).name
            return self.save_directory / f"{name}"
        except:
            pass
        return self.save_directory / f"/{uuid.uuid4()}"

    def _download(self, url):
        self._progress_bar.set_postfix_str(f"Downloading '{url}'")
        try:
            output_file = self._create_temp_file(like_url=url)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with output_file.open("wb") as handle:
                response = requests.get(url, stream=True)
                self._progress_bar.set_postfix_str(f"Saving '{output_file}'")
                if not response.ok:
                    raise IOError(f"Could not download url '{url}'")
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            output_file = str(output_file)
        except:
            self._progress_bar.set_postfix_str(f"Failed to download '{url}'")
            output_file = url
        self._progress_bar.update()
        return url, output_file

    def get(self, number_of_processes=None):
        if number_of_processes is None:
            number_of_processes = min(available_cpu_count(), 8)
        return ThreadPool(number_of_processes).imap_unordered(self._download, self._urls)

    def get_all(self, number_of_processes=None):
        thread_pool = self.get(number_of_processes)
        results = dict(thread_pool)
        self._progress_bar.set_postfix_str(f"Saved data to '{self.save_directory}'")
        return results
