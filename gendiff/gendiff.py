"""

This module implements generate diff logic.

"""

from functools import reduce

from gendiff import model, fetcher, parser
from gendiff.formatters import get_formatter


def generate_diff(path1: str, path2: str, format_: str = 'stylish') -> str:
    """Returns formatted diff betwee data from path1 and path2."""
    raw_data1, data_format1 = fetcher.fetch(path1)
    raw_data2, data_format2 = fetcher.fetch(path2)

    data1 = parser.parse(raw_data1, data_format1)
    data2 = parser.parse(raw_data2, data_format2)

    diff = gen_diff(data1, data2)

    formatter = get_formatter(format_)

    return formatter.stringify(diff)


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
    children = reduce(walk, all_keys, {})
    return model.make_nested(children)
