#
#  Pysocket Template
#  Template classes for Python socket applications.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import json
from typing import Any, Union


class DataMan:
    def __init__(self, base_path: str) -> None:
        """
        Initializes data manager.
        :param base_path: Base path of all data.
        """
        self.base_path = base_path

    def read(self, path: str, mode: str = "r") -> Union[str, bytes]:
        with open(os.path.join(self.base_path, path), mode) as file:
            return file.read()

    def write(self, text: Union[str, bytes], path: str, mode: str = "w") -> None:
        with open(os.path.join(self.base_path, path), mode) as file:
            file.write(text)

    def isfile(self, path: str) -> bool:
        return os.path.isfile(os.path.join(self.base_path, path))

    def isdir(self, path: str) -> bool:
        return os.path.isdir(os.path.join(self.base_path, path))

    def makedirs(self, path: str, exist_ok: bool) -> None:
        os.makedirs(os.path.join(self.base_path, path), exist_ok=exist_ok)

    def load(self, path: str) -> Any:
        with open(os.path.join(self.base_path, path), "r") as file:
            return json.load(file)

    def dump(self, obj: Any, path: str) -> None:
        with open(os.path.join(self.base_path, path), "w") as file:
            json.dump(obj, file)
