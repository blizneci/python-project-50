"""

This module implements plain text formatter for diff.

"""

from functools import reduce
from typing import Callable

from termcolor import colored

from gendiff import model

ADDED_TEMPLATE = 'Property {key} was added with value: {value}'
REMOVED_TEMPLATE = 'Property {key} was removed'
CHANGED_TEMPLATE = 'Property {key!r} was updated. From {removed} to {added}'


def stringify(diff: Callable, path: list = None) -> list[str] | str:
    if path is None:
        path = list()

    def walk(acc, item):
        key, node = item
        next_path = path + [key]
        type_ = model.get_type(node)
        match type_:
            case model.UNCHANGED:
                return acc
            case model.NESTED:
                line = stringify(node, next_path)
            case _:
                line = form_line(next_path, type_, node)
        acc.append(line)
        return acc

    children = model.get_children(diff)
    acc = reduce(walk, sorted(children.items()), list())
    return '\n'.join(acc)


def form_line(next_path: list[str], type_: str, node: Callable) -> str:
    key = '.'.join(next_path)
    match type_:
        case model.ADDED:
            value = model.get_value(node)
            return ADDED_TEMPLATE.format(
                key=colored(repr(key), 'light_green'),
                value=colored(to_string(value), 'light_green'),
            )
        case model.REMOVED:
            return REMOVED_TEMPLATE.format(key=colored(repr(key), 'light_red'))
        case model.CHANGED:
            removed = model.get_removed(node)
            added = model.get_added(node)
            line = CHANGED_TEMPLATE.format(
                key=key,
                removed=colored(to_string(removed), 'light_red'),
                added=colored(to_string(added), 'light_green'),
            )
            return line


def to_string(value):
    match value:
        case None:
            return 'null'
        case dict(value) | list(value):
            return '[complex value]'
        case bool(value):
            return str(value).lower()
        case str(value):
            return repr(value)
    return value
