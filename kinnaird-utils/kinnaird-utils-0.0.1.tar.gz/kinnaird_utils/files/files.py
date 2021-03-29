import logging
import csv
import json
import yaml

logger = logging.getLogger(__name__)


def read_yaml_file(filename: str) -> dict:
    """
    Reads a YAML file, safe loads, and returns the dictionary

    :param filename: name of the yaml file
    :return: dictionary of YAML file contents
    """
    with open(filename, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            logger.critical(exc)
    return cfg


def read_csv_file(filename: str, delimiter: str = ",") -> list:
    results = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        for row in csv_reader:
            results.append(row)
    return results


def read_json_file(file: str) -> dict:
    with open(file) as f:
        contents = f.read()
        try:
            results = json.loads(contents)
        except json.decoder.JSONDecodeError as error:
            logger.debug(error)
            decoded_data = contents.encode().decode("utf-8-sig")
            results = json.loads(decoded_data)
    return results
