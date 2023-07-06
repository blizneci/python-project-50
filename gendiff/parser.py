import json
import yaml
from yaml import Loader


def parse(path: str) -> dict | list:
    if path.endswith(('.yaml', '.yml')):
        return yaml.load(open(path, 'r'), Loader=Loader)
    return json.load(open(path, 'r'))


# def get_(data: dict | list[any], key: any) -> any:
#     """Returns value from file data."""
#     if not in_(data, key):
#         return None
#     return data[key]


# def in_(data: dict | list, key: any) -> bool:
#     """Checks if the key in the data."""
#     if isinstance(data, dict):
#         return key in data
#     return key < len(data)
#
#
# def is_dicts(data1: dict | list[any], data2: dict | list[any]) -> bool:
#     """Checks if the both data are dicts."""
#     return isinstance(data1, dict) and isinstance(data2, dict)
#
#
# def is_lists(data1: dict | list[any], data2: dict | list[any]) -> bool:
#     """Checks if the both data are lists."""
#     return isinstance(data1, list) and isinstance(data2, list)
#
#
# def is_both_nested(data1, data2):
#     return is_dicts(data1, data2) or is_lists(data1, data2)
