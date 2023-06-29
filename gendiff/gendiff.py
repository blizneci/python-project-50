"""

This module implements generate diff logic.

"""


from functools import reduce

from gendiff.parser import parse, get_, in_, is_dicts, is_lists
from gendiff.model import make_diff_view, make_node, get_sorted_keys
from gendiff.formatter import format_output, stringify


def generate_diff(
        file_path1: str,
        file_path2: str,
        output_format: str = 'stylish') -> str:
    """Returns formatted diff from data1 and data2."""

    data1 = parse(file_path1)
    data2 = parse(file_path2)

    diff = gen_diff(data1, data2)

    #formatted_output = format_output(diff, output_format)
    formatted_output = stringify(diff)

    return formatted_output


def gen_diff(data1: dict | list, data2: dict | list) -> dict | list:
    """Returns a diff from data1 and data2."""
    if not (is_dicts(data1, data2) or is_lists(data1, data2)):
        return data1

    diff = make_diff_view(data1, data2)
    keys = get_sorted_keys(diff)

    def fill(diff, key):
        value1 = get_(data1, key)
        value2 = get_(data2, key)
        if not in_(data1, key):
            diff[key] = make_node('added', gen_diff(value2, value2))
        elif not in_(data2, key):
            diff[key] = make_node('deleted', gen_diff(value1, value1))
        elif is_dicts(value1, value2) or is_lists(value1, value2):
            diff[key] = make_node('nested', gen_diff(value1, value2))
        elif value1 == value2:
            diff[key] = make_node('unchanged', gen_diff(value1, value1))
        else:
            diff[key] = make_node('changed', (
                        gen_diff(value1, value1),
                        gen_diff(value2, value2),
                        ),
                    )
        return diff

    diff = reduce(fill, keys, diff)
    return diff
