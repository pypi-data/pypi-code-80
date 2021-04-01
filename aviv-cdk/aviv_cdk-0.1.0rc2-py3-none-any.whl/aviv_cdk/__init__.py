__version__='0.1.0rc2'


def json_load(filename: str) -> dict:
    import json
    with open(filename) as cfgfile:
        return json.load(cfgfile)

def load_yaml(filename: str) -> object:
    import yaml
    with open(filename, encoding="utf8") as fp:
        with fp.read() as bsfile:
            return yaml.safe_load(bsfile)
