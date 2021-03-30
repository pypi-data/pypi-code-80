import os
from pathlib import Path
import json
from khquizgen import logger, INPUTS_PATH, OUTPUTS_PATH


def run(inputs_path=None, outputs_path = None):
    """
    Get the data and preprocess it appropriately
    """
    inputs_path = inputs_path if inputs_path else INPUTS_PATH
    outputs_path = outputs_path if outputs_path else OUTPUTS_PATH
    raw_data = get_raw_data(inputs_path)
    root = parse_q(raw_data)
    save_j_data(root, outputs_path)
    return root


def get_raw_data(InputsPath):
    """
    Get the data from the data.csv file inside the folder
    """
    in_file = Path.resolve(InputsPath.joinpath('questions.txt'))
    with open(in_file, 'r') as file:
        data = file.read()
    return data


def parse_q(raw_data : str):
    s_test = raw_data.splitlines()
    root, trunk_d, branch_d = {}, {}, {}
    trunk, branch, leaf = None, None, None
    for line in s_test:
        line = line.strip()
        if ':::' in line:

            if trunk:
                trunk_d[branch] = branch_d
                root[trunk] = trunk_d
                branch, leaf = None, None
                branch_d, trunk_d = {}, {}

            trunk = line.split(':::')[0].strip()

        elif '::' in line:
            if branch:
                trunk_d[branch] = branch_d
                branch_d = {}
            branch = line.split('::')[0].strip()

        elif ':' in line:
            leaf = line.split(':')
            if leaf[1]:
                if ',' in leaf[1]:
                    leaf[1] = leaf[1].split(',')
                    leaf[1] = [x.strip() for x in leaf[1]]
                else:
                    leaf[1] = [leaf[1].strip()]
            else:
                leaf[1] = []
            branch_d[leaf[0]] = leaf[1]

        elif '$$$$' in line:
            trunk_d[branch] = branch_d
            root[trunk] = trunk_d
        else:
            pass
    return root


def save_j_data(j_data, OutputsPath):
    out_file = Path.resolve(OutputsPath.joinpath('questions.json'))
    with open(out_file, 'w') as file:
        json.dump(j_data, indent=3, fp=file)
