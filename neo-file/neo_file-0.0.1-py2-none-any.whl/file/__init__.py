def load(file_name):
    file_type = str(file_name).split('.')[-1]
    if file_type == 'csv':
        return load_csv(file_name)
    if file_type == 'json':
        return load_json(file_name)
    raise Exception


def load_csv(file_name):
    import csv
    import copy
    result = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(copy.copy(row))
    return result


def load_json(file_name):
    import json
    with open(file_name, 'r') as f:
        return json.load(f)


def dump(file_content, file_path):
    file_type = str(file_path).split('.')[-1]
    if file_type == 'csv':
        return dump_csv(file_content, file_path)
    if file_type == 'json':
        return dump_json(file_content, file_path)
    raise Exception


def dump_csv(file_content, file_path):
    import csv
    with open(file_path, 'w') as f:
        csv.writer(f).writerows(file_content)


def dump_json(file_content, file_path):
    import json
    with open(file_path, 'w') as f:
        json.dump(file_content, f)
