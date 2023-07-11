"""

This module implements a stylish formatter.

"""

from functools import reduce
from itertools import chain

from termcolor import colored

from gendiff import model


INDENT_SIZE = 4


def stringify(diff, lvl=0):
    if diff is None:
        return 'null'
    elif isinstance(diff, bool):
        return str(diff).lower()
    elif not (isinstance(diff, dict) or model.is_diff(diff)):
        return diff

    indent = INDENT_SIZE * (lvl + 1)

    def walk(acc, item):
        key, node = item
        status = get_status(node)
        match status:
            case model.CHANGED:
                removed = stringify(model.get_removed(node), lvl + 1)
                removed_line = form_line(indent, model.REMOVED, key, removed)

                added = stringify(model.get_added(node), lvl + 1)
                added_line = form_line(indent, model.ADDED, key, added)

                acc.extend((removed_line, added_line))
                return acc
            case model.UNCHANGED | model.ADDED | model.REMOVED:
                value = stringify(model.get_value(node), lvl + 1)
            case model.NESTED | None:
                value = stringify(node, lvl + 1)
        line = form_line(indent, status, key, value)
        acc.append(line)
        return acc

    children = get_children(diff)
    cur_lvl = reduce(walk, sorted(children.items()), list())
    indent -= INDENT_SIZE
    result = chain('{', cur_lvl, ['}'.rjust(indent + 1)])
    return '\n'.join(result)


def get_status(node):
    if model.is_diff(node):
        return model.get_status(node)


def get_children(node):
    if model.is_diff(node):
        return model.get_children(node)
    return node


def form_line(indent, status, key, value):
    sign, color = get_sign_and_color(status)
    formatted_indent = f'{sign} '.rjust(indent)
    line = f'{formatted_indent}{key}: {value}'
    if color:
        return colored(line, color)
    return line


def get_sign_and_color(status):
    match status:
        case model.ADDED:
            return ('+', 'light_green')
        case model.REMOVED:
            return ('-', 'light_red')
    return (' ', None)
