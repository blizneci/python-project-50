import json
import yaml
from yaml import Loader


def parse(path: str) -> dict | list:
    """Reads data from the file and returns it as a dictionary."""
    if path.endswith(('.yaml', '.yml')):
        return yaml.load(open(path, 'r'), Loader=Loader)
    return json.load(open(path, 'r'))
