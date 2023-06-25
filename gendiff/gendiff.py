import itertools
import json
import os


def generate_diff(path1: str, path2: str) -> str:
    if not (os.path.exists(path1) and os.path.exists(path2)):
        print('Files have to exist.')
        return
    data1 = json.load(open(path1, 'r'))
    data2 = json.load(open(path2, 'r'))
    diff_data = gen_diff(data1, data2)
    diff_formatted = stringify(diff_data, data1, data2)
    return diff_formatted


def gen_diff(data1, data2):
    diff_data = dict()
    all_keys = data1.keys() | data2.keys()
    for key in all_keys:
        value1 = data1.get(key, None)
        value2 = data2.get(key, None)

        if key not in data1:
            diff_data[key] = 'added'
        elif key not in data2:
            diff_data[key] = 'deleted'
        elif isinstance(value1, dict) and isinstance(value2, dict):
            diff_data[key] = gen_diff(
                    data1.get(key),
                    data2.get(key),
                    )
        elif value1 == value2:
            diff_data[key] = 'unchanged'
        else:
            diff_data[key] = 'changed'
    return diff_data


def stringify(diff_data, data1, data2, replacer=' ', cnt_spaces=4):

    def walk(node, level, data1, data2):
        if not isinstance(node, dict):
            return str(node)

        next_indent_size = cnt_spaces * (level + 1)
        cur_level = list()

        for diff_key, diff_value in sorted(node.items(), key=str):
            if isinstance(diff_value, dict):
                sign = '  '
                value = walk(
                        diff_value,
                        level + 1,
                        data1.get(diff_key, dict()),
                        data2.get(diff_key, dict()),
                        )
            elif diff_value == 'deleted':
                sign = '- '
                value = data1.get(diff_key)
            elif diff_value == 'added':
                sign = '+ '
                value = data2.get(diff_key)
            elif diff_value == 'unchanged':
                sign = '  '
                value = data1.get(diff_key)
            else:
                value1 = data1.get(diff_key)
                value2 = data2.get(diff_key)
                value = (value1, value2)

            if isinstance(value, tuple):
                value1, value2 = value
                value1 = to_json_format(value1)
                value2 = to_json_format(value2)
                cur_level.extend((
                    format_line("- ", next_indent_size, diff_key, value1),
                    format_line("+ ", next_indent_size, diff_key, value2),
                    ))
            else:
                value = to_json_format(value)
                cur_level.append(
                        format_line(sign, next_indent_size, diff_key, value),
                        )

        indent = replacer * cnt_spaces * level
        result = itertools.chain('{', cur_level, [indent + '}'])
        return '\n'.join(result)
    return walk(diff_data, 0, data1, data2)


def format_line(sign, indent_size, key, value):
    return f'{sign:>{indent_size}}{key}: {value}'


def to_json_format(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return value


if __name__ == '__main__':
    from pprint import pprint
    data1 = {
        "string": "value",
        "boolean": True,
        "number": 5,  # deleted
        "dict": {
            5: "number",
            None: None,
            True: "boolean",
            "value": "string",
            "nested": {
                "boolean": True,
                "string": 'value',
                "number": 5,
                None: None,  # deleted
            },
        },
    }

    data2 = {
        "string": "new_value",  # changed
        "boolean": True,
        "dict": {
            5: "number",
            None: None,
            True: "boolean",
            "value": "string",
            "replacer": "|-",  # added
            "nested": {
                "boolean": True,
                "string": 'value',
                "number": 1,  # changed
            },
        },
    }

    diff_data = gen_diff(data1, data2)
    pprint(diff_data)
    diff_str = stringify(diff_data, data1, data2)
    print(diff_str)
    print(json.dumps(data1))
