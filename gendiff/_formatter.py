from itertools import chain

from termcolor import colored

from _model import *


INDENT_SIZE = 4
STATUSES = {
        'added': ('+ ', 'green'),
        'removed': ('- ', 'red'),
        None: ('  ', None),
        }


def form_line(indent, status, key, value):
    sign, color = STATUSES.get(status)
    line = f'{sign:>{indent}}{key}: {value}'
    if color:
        return colored(line, color)
    return line


def stylish(diff):
    def walk(node, lvl=0):
        if isinstance(node, dict):
            for 
        indent = INDENT_SIZE * (lvl + 1)

    if isinstance(diff, dict):

def _stylish(diff):

    def walk(node, lvl=0):
        children = get_children(node)
        indent = INDENT_SIZE * (lvl + 1)
        cur_level = list()

        for key, cur_node in sorted(children.items()):
            if is_nested(cur_node):
                value = walk(cur_node, lvl + 1)
                value = stringify(value, lvl + 1)
                sign = '  '
                line = f'{sign:>{indent}}{key}: {value}'
                cur_level.append(line)
            elif is_changed(cur_node):
                removed_value = get_removed_value(cur_node)
                removed_value = stringify(removed_value, lvl + 1)
                sign = '- '
                color = 'red'
                line = f'{sign:>{indent}}{key}: {removed_value}'
                cur_level.append(colored(line, color))
                added_value = get_added_value(cur_node)
                added_value = stringify(added_value, lvl + 1)
                sign = '+ '
                color = 'green'
                line = f'{sign:>{indent}}{key}: {added_value}'
                cur_level.append(colored(line, color))
            else:
                status = get_status(cur_node)
                value = get_value(cur_node)
                value = stringify(value, lvl + 1)
                if status == 'added':
                    sign = '+ '
                    color = 'green'
                elif status == 'removed':
                    sign = '- '
                    color = 'red'
                else:
                    sign = '  '
                    color = None
                line = f'{sign:>{indent}}{key}: {value}'
                if color is not None:
                    cur_level.append(colored(line, color))
                else:
                    cur_level.append(line)

        indent = INDENT_SIZE * lvl
        result = chain('{', cur_level, ['}'.rjust(indent + 1)])
        return '\n'.join(result)
    return walk(diff, 0)


def _stringify(data, lvl):
    if not isinstance(data, dict):
        if data is None:
            return "null"
        elif isinstance(data, bool):
            return str(data).lower()
        else:
            return str(data)
    indent = INDENT_SIZE * (lvl + 1)
    cur_lvl = list()
    for key, value in data.items():
        value = stringify(value, lvl + 1)
        line = f'{"".rjust(indent)}{key}: {value}'
        cur_lvl.append(line)

    indent = INDENT_SIZE * lvl
    result = chain('{', cur_lvl, ['}'.rjust(indent + 1)])
    return '\n'.join(result)


from _gendiff import *
s = stylish(diff)
