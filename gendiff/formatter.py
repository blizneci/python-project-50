import json

from functools import reduce
from itertools import chain

from termcolor import colored

from gendiff import model


INDENT_SIZE = 4
STATUSES = {
        model.ADDED: ('+', 'green'),
        model.REMOVED: ('-', 'red'),
        }
ADDED_TEMPLATE = 'Property {key} was added with value: {value}'
REMOVED_TEMPLATE = 'Property {key} was removed'
CHANGED_TEMPLATE = 'Property {key} was updated. From {removed} to {added}'


def get_formatter(output_format):
    match output_format:
        case 'stylish':
            return stylish
        case 'plain':
            return plain
        case 'json':
            return json_


def stylish(diff, lvl=0):
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
                removed = stylish(model.get_removed(node), lvl + 1)
                removed_line = form_line(indent, model.REMOVED, key, removed)

                added = stylish(model.get_added(node), lvl + 1)
                added_line = form_line(indent, model.ADDED, key, added)

                acc.extend((removed_line, added_line))
                return acc
            case model.UNCHANGED | model.ADDED | model.REMOVED:
                value = stylish(model.get_value(node), lvl + 1)
            case model.NESTED | None:
                value = stylish(node, lvl + 1)
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
    sign, color = STATUSES.get(status, (' ', None))
    formatted_indent = f'{sign} '.rjust(indent)
    line = f'{formatted_indent}{key}: {value}'
    if color:
        return colored(line, color)
    return line

def _stringify(value):
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (dict, list)):
        return '[complex value]'
    return str(value)

def stringify(value):
    match value:
        case None:
            return 'null'
        case dict(value) | list(value):
            return '[complex value]'
        case bool(value):
            return str(value).lower()
    return str(value)


def plain(diff, key_path=None):
    if not model.is_diff(diff):
        return stringify(diff)

    if key_path is None:
        key_path = list()

    def walk(acc, item):
        key, node = item
        status = get_status(node)
        next_path = key_path + [key]
        match status:
            case model.ADDED | model.REMOVED:
                value = model.get_value(node)
                line = form_plain_line(next_path, status, value)
                acc.append(line)
            case model.CHANGED:
                value = (model.get_removed(node), model.get_added(node))
                line = form_plain_line(next_path, status, value)
                acc.append(line)
            case model.NESTED:
                acc.extend(plain(node, next_path))
        return acc

    children = get_children(diff) 
    acc = reduce(walk, sorted(children.items()), list())
    if not key_path:
        return '\n'.join(acc)
    return result


def json_(diff):
    transformed_diff = model.to_dict(diff)
    return json.dumps(transformed_diff, sort_keys=True, indent=4)
