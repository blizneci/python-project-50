"""

This module implements generate diff logic.

"""

from functools import reduce

from gendiff import parser
from gendiff import model
from gendiff.formatters import get_formatter


def generate_diff(
        file_path1: str,
        file_path2: str,
        _format: str = 'stylish') -> str:
    """Returns formatted diff from data1 and data2."""

    data1 = parser.parse(file_path1)
    data2 = parser.parse(file_path2)

    diff = gen_diff(data1, data2)

    formatter = get_formatter(_format)

    stringified_diff = formatter.stringify(diff)

    return stringified_diff


def gen_diff(data1, data2):
    if not (isinstance(data1, dict) and isinstance(data2, dict)):
        if data1 != data2:
            return model.make_changed(data1, data2)
        return model.make_unchanged(data1)

    def walk(acc, key):
        if key not in data1:
            acc[key] = model.make_added(data2.get(key))
        elif key not in data2:
            acc[key] = model.make_removed(data1.get(key))
        else:
            value1 = data1.get(key)
            value2 = data2.get(key)
            acc[key] = gen_diff(value1, value2)
        return acc

    all_keys = data1.keys() | data2.keys()
    children = reduce(walk, all_keys, dict())
    return model.make_nested(children)
