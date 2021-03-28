import inspect
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, List

from mosaik_multi_project.multi_project.util.paths import DATA_PATH


def load_simulators(
    *,
    configuration_file_paths: List[Path],
) -> List[Dict]:
    simulators: List[Dict] = []
    for configuration_file_path in configuration_file_paths:
        with open(DATA_PATH / configuration_file_path, 'r') as config_file:
            try:
                simulators += json.load(config_file)['projects']
            except (JSONDecodeError, TypeError) as malformed_json_error:
                print(
                    'Error: '
                    'A function encountered an error where the '
                    'data being deserialized is not a valid JSON document. '
                    'The function:', inspect.stack()[0][3],
                    'The document:', config_file
                )
                raise malformed_json_error

    return simulators
