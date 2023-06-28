from itertools import chain
from functools import reduce
from typing import Iterable

from termcolor import colored

from gendiff.model import get_sorted_keys


INDENT_SIZE = 4
STATUSES = {
        'added': ('+ ', 'green'),
        'deleted': ('- ', 'red'),
        'unchanged': ('  ', None),
        'nested': ('  ', None),
        }


def format_output(diff, output_format='json'):
    print(stringify(diff))


def stringify(diff, lvl=0):
    if not isinstance(diff, (dict, list)):
        return str(diff)

    keys = get_sorted_keys(diff)
    indent = INDENT_SIZE * (lvl + 1)

    def cur_lvl_str(key):
        node = diff[key]
        status = get_status(node)
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
            raw_value = get_value(node)
            value = to_json_format(value)
            sign, color = STATUSES.get(status)
            line = colored(form_line(indent, sign, key, value), color)
            acc.append(line)
        return acc

    cur_lvl_str = map(generate_string, keys)
    indent = lvl_size * lvl + 1
    open_bracket, close_bracket = '[]' if isinstance(diff, list) else '{}'

    result = chain(open_bracket, cur_lvl_str, [f'{close_bracket:>{indent}}'])
    return '\n'.join(result)


def form_line(indent: int, sign: str, key: str, value: any) -> str:
    return f'{sign:>{indent}}{key}: {value}'


def to_json_format(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        value = ', '.join(map(to_json_format, value))
        return f'[{value}]'
    if isinstance(value, dict):
        value = ', '.join(map(
            lambda key: f'{key}: {value[key]}',
            sorted(value.keys())
            ))
        return '{' + value + '}'
    return value
