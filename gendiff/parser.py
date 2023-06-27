import json
import yaml
from yaml import Loader


def get_data_from_file(path):
    if path.endswith(('.yaml', '.yml')):
        return yaml.load(open(path, 'r'), Loader=Loader)
    return json.load(open(path, 'r'))
