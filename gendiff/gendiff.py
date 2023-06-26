import json
import os

from itertools import chain
from functools import reduce
from typing import Iterable

from termcolor import colored


"""

This module implements generate diff logic.

"""


STATUSES = {
        'added': ('+ ', 'green'),
        'deleted': ('- ', 'red'),
        'unchanged': ('  ', None),
        'nested': ('  ', None),
        }


def generate_diff(path1: str, path2: str) -> str:
    """Returns stringified diff from data1 and data2."""
    if not (os.path.exists(path1) or os.path.exists(path2)):
        print('Files have to exist.')
        return

    data1 = json.load(open(path1))
    data2 = json.load(open(path2))

    diff = gen_diff(data1, data2)

    return stringify(diff)


def stringify(diff, lvl=0, lvl_size=4):
    if not isinstance(diff, (dict, list)):
        return str(diff)

    sorted_keys = get_keys(diff)
    indent = lvl_size * (lvl + 1)
    
    def fill_cur_level(acc, key):
        node = diff[key]
        status = node['status']
        value = node['value']
        if status == 'nested':
            value = stringify(value, lvl + 1)
        if status == 'changed':
            value1, value2 = value
            value1 = to_json_format(value1)
            value2 = to_json_format(value2)
            sign1, color1 = STATUSES.get('deleted')
            sign2, color2 = STATUSES.get('added')
            line1 = colored(form_line(indent, sign1, key, value1), color1)
            line2 = colored(form_line(indent, sign2, key, value2), color2)
            acc.extend((line1, line2))
        else:
            value = to_json_format(value)
            sign, color = STATUSES.get(status)
            line = colored(form_line(indent, sign, key, value), color)
            acc.append(line)
        return acc

    cur_level = reduce(fill_cur_level, sorted_keys, list())
    indent = lvl_size * lvl + 1

    if isinstance(diff, list):
        open_bracket, close_bracket  = '[]'
    elif isinstance(diff, dict):
        open_bracket, close_bracket  = '{}'

    result = chain(open_bracket, cur_level, [f'{close_bracket:>{indent}}'])
    return '\n'.join(result)


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


def get_keys(diff: dict | list) -> Iterable:
    return sorted(diff.keys()) if isinstance(diff, dict) else range(len(diff))


def form_line(indent: int, sign: str, key: str, value: any) -> str:
    return f'{sign:>{indent}}{key}: {value}'


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


# def get_diff_status(diff: dict, key: str) -> str:
#     """Returns a status of the given key in data."""
#     return diff[key]['status']


def make_node(status: str, value: any) -> dict:
    """Returns new diff node with status and value."""
    return {'status': status, 'value': value}


def is_dicts(data1: dict | list[any], data2: dict | list[any]) -> bool:
    """Checks if the both data are dicts."""
    return isinstance(data1, dict) and isinstance(data2, dict)


def is_lists(data1: dict | list[any], data2: dict | list[any]) -> bool:
    """Checks if the both data are lists."""
    return isinstance(data1, list) and isinstance(data2, list)


def to_json_format(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        value = ', ', join(map(to_json_format, value))
        return f'[{value}]'
    if isinstance(value, dict):
        value = ', '.join(map(lambda key: f'{key}: {value[key]}', sorted(value.keys())))
        return '{' + value + '}'
    return value
