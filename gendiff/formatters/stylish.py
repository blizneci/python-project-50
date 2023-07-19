"""

This module implements a stylish formatter.

"""

from functools import reduce
from itertools import chain
from typing import Callable

from termcolor import colored

from gendiff import model


INDENT_SIZE = 4


def stringify(diff: Callable, lvl: int = 0) -> str:
    """Returns stringified diff in stylish format."""
    def walk(acc, item):
        key, node = item
        type_ = model.get_type(node)
        match type_:
            case model.CHANGED:
                removed_line = form_line(lvl, model.REMOVED,
                                         key, model.get_removed(node))

                added_line = form_line(lvl, model.ADDED,
                                       key, model.get_added(node))

                acc.extend((removed_line, added_line))
                return acc
            case model.UNCHANGED | model.ADDED | model.REMOVED:
                line = form_line(lvl, type_, key, model.get_value(node))
            case model.NESTED:
                line = form_line(lvl, type_, key, stringify(node, lvl + 1))
        acc.append(line)
        return acc

    children = model.get_children(diff)
    cur_lvl = reduce(walk, sorted(children.items()), [])
    indent = INDENT_SIZE * lvl
    result = chain('{', cur_lvl, ['}'.rjust(indent + 1)])
    return '\n'.join(result)


def form_line(lvl: int, type_: str, key: str, value: any) -> str:
    """Returns a line in 'key: value' format."""
    sign, color = get_sign_and_color(type_)
    stringified_value = to_string(value, lvl + 1)
    indent = INDENT_SIZE * (lvl + 1)
    formatted_indent = f'{sign} '.rjust(indent)
    line = f'{formatted_indent}{key}: {stringified_value}'
    if color:
        return colored(line, color)
    return line


def get_sign_and_color(type_: str) -> tuple[str, str]:
    """Returns a tuple with indent sign and color description."""
    match type_:
        case model.ADDED:
            return ('+', 'light_green')
        case model.REMOVED:
            return ('-', 'light_red')
    return (' ', '')


def to_string(value: any, lvl: int):
    """Returns stringified value."""
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    if not isinstance(value, dict):
        return str(value)

    def walk(acc, item):
        key, value = item
        line = form_line(lvl, None, key, value)
        acc.append(line)
        return acc

    cur_lvl = reduce(walk, sorted(value.items()), [])
    indent = INDENT_SIZE * lvl
    result = chain('{', cur_lvl, ['}'.rjust(indent + 1)])
    return '\n'.join(result)
