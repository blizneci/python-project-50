"""

This module implements generate diff logic.

"""


from functools import reduce

from gendiff.parser import parse, get_, is_dicts, is_lists, is_both_nested
from gendiff.model import make_diff_view, get_sorted_keys
from gendiff.model import make_node, make_status
from gendiff.formatter import stringify


def generate_diff(
        file_path1: str,
        file_path2: str,
        output_format: str = 'stylish') -> str:
    """Returns formatted diff from data1 and data2."""

    data1 = parse(file_path1)
    data2 = parse(file_path2)

    diff = gen_diff(data1, data2)

    formatted_output = stringify(diff)

    return formatted_output


def gen_diff(data1: dict | list, data2: dict | list = None) -> dict | list:
    """Returns a diff from data1 and data2."""
    if data2 is None:
        data2 = data1
    if not (is_dicts(data1, data2) or is_lists(data1, data2)):
        return data1

    diff = make_diff_view(data1, data2)
    keys = get_sorted_keys(diff)

    def fill(diff, key):
        value1 = get_(data1, key)
        value2 = get_(data2, key)
        node_status = make_status(data1, data2, key)
        if node_status is not None:
            value = value1 if node_status == 'deleted' else value2
            diff[key] = make_node(node_status, gen_diff(value))
        elif is_both_nested(value1, value2) or value1 == value2:
            diff[key] = make_node(node_status, gen_diff(value1, value2))
        else:
            diff[key] = make_node('changed', (
                        gen_diff(value1),
                        gen_diff(value2),
                        ))
        return diff

    diff = reduce(fill, keys, diff)
    return diff
