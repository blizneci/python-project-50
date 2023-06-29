from typing import Iterable

from gendiff.parser import in_, is_dicts, is_lists


def make_diff_view(
        data1: dict | list[any],
        data2: dict | list[any],
        ) -> tuple:
    """Returns empty diff view"""
    if is_dicts(data1, data2):
        return dict.fromkeys(data1.keys() | data2.keys(), None)
    elif is_lists(data1, data2):
        return [None] * max(len(data1), len(data2))


def get_sorted_keys(diff: dict | list) -> Iterable:
    if isinstance(diff, dict):
        return sorted(diff.keys(), key=str)
    return range(len(diff))


def make_node(status: str, value: any) -> dict:
    """Returns new diff node with status and value."""
    node = {'status': status}
    if isinstance(value, tuple):
        value1, value2 = value
        node['deleted_value'] = value1
        node['added_value'] = value2
    else:
        node['value'] = value
    return node


def make_status(data1, data2, key):
    if not in_(data1, key):
        return 'added'
    if not in_(data2, key):
        return 'deleted'
    return None
