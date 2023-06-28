from typing import Iterable


def make_diff_view(
        data1: dict | list[any],
        data2: dict | list[any],
        ) -> tuple:
    """Returns empty diff view"""
    if isinstance(data1, dict) and isinstance(data2, dict):
        return dict.fromkeys(data1.keys() | data2.keys(), None)
    elif isinstance(data1, list) and isinstance(data2, list):
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
        node['old_value'] = value1
        node['new_value'] = value2
    else:
        node['value'] = value
    return node


def get_value(node):
    if get_status(node) == 'changed':
        return node['old_value'], node['new_value']
    else:
        return node['value']
