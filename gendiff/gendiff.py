"""

This module implements generate diff logic.

"""


from functools import reduce

from gendiff.parser import get_data_from_file
from gendiff.formatter import stringify


def generate_diff(path1: str, path2: str) -> str:
    """Returns stringified diff from data1 and data2."""

    data1 = get_data_from_file(path1)
    data2 = get_data_from_file(path2)

    diff = gen_diff(data1, data2)

    return stringify(diff)


def gen_diff(data1: dict | list, data2: dict | list) -> dict | list:
    """Returns a diff from data1 and data2."""
    diff, all_keys = create_empty_diff(data1, data2)

    def fill(diff, key):
        value1 = get_value(data1, key)
        value2 = get_value(data2, key)
        if not in_(data1, key):
            diff[key] = make_node('added', value2)
        elif not in_(data2, key):
            diff[key] = make_node('deleted', value1)
        elif is_dicts(value1, value2) or is_lists(value1, value2):
            diff[key] = make_node('nested', gen_diff(value1, value2))
        elif value1 == value2:
            diff[key] = make_node('unchanged', value1)
        else:
            diff[key] = make_node('changed', (value1, value2))
        return diff

    diff = reduce(fill, all_keys, diff)
    return diff


def create_empty_diff(
        data1: dict | list[any],
        data2: dict | list[any]) -> tuple:
    """Returns empty diff"""

    if is_dicts(data1, data2):
        return dict(), data1.keys() | data2.keys()
    length = max(len(data1), len(data2))
    diff = [None for i in range(length)]
    return diff, range(length)


def get_value(data: dict | list[any], key: str) -> any:
    """Returns value from file data."""
    if not in_(data, key):
        return None
    return data[key]


def in_(data: dict | list, key: str) -> bool:
    """Checks if the key in the data."""
    if isinstance(data, dict):
        return key in data
    return key < len(data)


def make_node(status: str, value: any) -> dict:
    """Returns new diff node with status and value."""
    return {'status': status, 'value': value}


def is_dicts(data1: dict | list[any], data2: dict | list[any]) -> bool:
    """Checks if the both data are dicts."""
    return isinstance(data1, dict) and isinstance(data2, dict)


def is_lists(data1: dict | list[any], data2: dict | list[any]) -> bool:
    """Checks if the both data are lists."""
    return isinstance(data1, list) and isinstance(data2, list)
