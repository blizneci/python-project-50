from gendiff.parser import parse
from gendiff._model import make_added, make_removed, make_nested, set_child
from gendiff._model import make_changed, make_unchanged
from gendiff._formatter import stylish


def generate_diff(
        file_path1: str,
        file_path2: str,
        output_format: str = 'stylish') -> str:
    """Returns formatted diff from data1 and data2."""

    data1 = parse(file_path1)
    data2 = parse(file_path2)

    diff = gen_diff(data1, data2)

    formatted_output = stylish(diff)

    return formatted_output


def gen_diff(data1, data2):
    if isinstance(data1, dict) and isinstance(data2, dict):
        node = make_nested()

        all_keys = data1.keys() | data2.keys()

        for key in all_keys:
            value1 = data1.get(key)
            value2 = data2.get(key)
            if key not in data1:
                child_node = make_added(value2)
            elif key not in data2:
                child_node = make_removed(value1)
            else:
                child_node = gen_diff(value1, value2)
            set_child(node, key, child_node)

        return node

    if data1 != data2:
        return make_changed(data1, data2)
    else:
        return make_unchanged(data1)
