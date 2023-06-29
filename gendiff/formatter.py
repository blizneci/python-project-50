from itertools import chain
from functools import reduce

from termcolor import colored

from gendiff.model import get_sorted_keys


INDENT_SIZE = 4
STATUSES = {
        'added': ('+ ', 'green'),
        'deleted': ('- ', 'red'),
        'unchanged': ('  ', None),
        'nested': ('  ', None),
        }


def format_output(diff, output_format='stylish'):
    print(stringify(diff))


def stringify(diff, lvl=0):
    if not (isinstance(diff, dict) or isinstance(diff, list)):
        return to_json_format(diff)

    keys = get_sorted_keys(diff)
    indent = INDENT_SIZE * (lvl + 1)

    def generate_string(acc, key):
        node = diff[key]
        status = node['status']
        if status == 'changed':
            sign, color = STATUSES.get('deleted')
            deleted_value = stringify(node['deleted_value'], lvl + 1)
            deleted_line = form_line(indent, sign, key, deleted_value)
            acc.append(colored(deleted_line, color))

            sign, color = STATUSES.get('added')
            added_value = stringify(node['added_value'], lvl + 1)
            added_line = form_line(indent, sign, key, added_value)
            acc.append(colored(added_line, color))
        else:
            sign, color = STATUSES.get(status)
            value = stringify(node['value'], lvl + 1)
            line = form_line(indent, sign, key, value)
            if color:
                acc.append(colored(line, color))
            else:
                acc.append(line)
        return acc

    cur_lvl = reduce(generate_string, keys, list())
    indent = INDENT_SIZE * lvl
    open_bracket, close_bracket = '[]' if isinstance(diff, list) else '{}'

    result = chain(open_bracket, cur_lvl, [close_bracket.rjust(indent + 1)])
    return '\n'.join(result)


def form_line(indent: int, sign: str, key: str, value: any) -> str:
    return f'{sign:>{indent}}{key}: {value}'


def to_json_format(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return value
