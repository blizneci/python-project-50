"""

This module implements generate diff logic.

"""


from gendiff import parser
from gendiff import model
from gendiff import formatter


def generate_diff(
        file_path1: str,
        file_path2: str,
        _format: str = 'stylish') -> str:
    """Returns formatted diff from data1 and data2."""

    data1 = parser.parse(file_path1)
    data2 = parser.parse(file_path2)

    diff = gen_diff(data1, data2)

    output_formatter = formatter.get_formatter(_format)

    formatted_output = output_formatter(diff)

    return formatted_output


def gen_diff(data1, data2):
    if isinstance(data1, dict) and isinstance(data2, dict):
        node = model.make_nested()

        all_keys = data1.keys() | data2.keys()

        for key in all_keys:
            value1 = data1.get(key)
            value2 = data2.get(key)
            if key not in data1:
                child_node = model.make_added(value2)
            elif key not in data2:
                child_node = model.make_removed(value1)
            else:
                child_node = gen_diff(value1, value2)
            model.set_child(node, key, child_node)

        return node

    if data1 != data2:
        return model.make_changed(data1, data2)
    else:
        return model.make_unchanged(data1)
