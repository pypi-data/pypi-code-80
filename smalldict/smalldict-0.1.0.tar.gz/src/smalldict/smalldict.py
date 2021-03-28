from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class SmallDict:
    """`SmallDict`

    Args:
        d: The source data, typically a nested dict and/or list, or
            path to a file, either JSON (`.json`) or YAML (`.yaml`, `.yml`).
    """

    d: Any

    def get(
        self,
        dict_limit: int = None,
        list_limit: int = None,
        str_limit: int = None,
        json_out: str = None,
        yaml_out: str = None,
    ) -> Any:
        """Apply limit to the source data recursively for dict or list.

        Args:
            dict_limit: Limit number of dict items. Defaults to None.
            list_limit: Limit number of list items. Defaults to None.
            str_limit: Limit length for str values. Defaults to None.
            json_out: Path to the output JSON file. Defaults to None.
            yaml_out: Path to the output YAML file. Defaults to None.

        Returns:
            The processed data.
        """
        d = self.d

        if isinstance(d, str) and Path(d).is_file():

            if Path(d).suffix in {".json"}:
                import json

                with open(d) as f:
                    d = json.load(f)

            elif Path(d).suffix in {".yaml", ".yml"}:
                import yaml

                with open(d) as f:
                    d = yaml.safe_load(f)

        d = slim_dict(d, dict_limit, list_limit, str_limit)

        if json_out:
            import json

            with open(json_out, mode="w") as f:
                json.dump(d, f)

        if yaml_out:
            import yaml

            with open(yaml_out, mode="w") as f:
                yaml.dump(d, f)

        return d


def slim_dict(
    d: Any, dict_limit: int = None, list_limit: int = None, str_limit: int = None
) -> Any:
    """Apply limit to the source data recursively for dict or list.

    Args:
        d: The source data, typically a nested dict and/or list.
        dict_limit: Limit number of dict items. Defaults to None.
        list_limit: Limit number of list items. Defaults to None.
        str_limit: Limit length for str values. Defaults to None.

    Returns:
        The processed data.
    """

    if isinstance(d, dict):
        dict_limit = len(d) if dict_limit is None else dict_limit
        return {
            k: slim_dict(v, dict_limit, list_limit, str_limit)
            for (k, v) in list(d.items())[:dict_limit]
        }

    if isinstance(d, list):
        list_limit = len(d) if list_limit is None else list_limit
        return [slim_dict(e, dict_limit, list_limit, str_limit) for e in d[:list_limit]]

    if isinstance(d, str):
        str_limit = len(d) if str_limit is None else str_limit
        return d[:str_limit]

    return d
