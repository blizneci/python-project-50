from functools import reduce
from itertools import chain

from termcolor import colored

from gendiff import model


INDENT_SIZE = 4
STATUSES = {
        model.ADDED: ('+', 'green'),
        model.REMOVED: ('-', 'red'),
        }


def get_formatter(output_format):
    match output_format:
        case 'stylish':
            return stylish
        case 'plain':
            return plain
        case 'json':
            return json_


def stylish(diff, lvl=0):
    indent = INDENT_SIZE * (lvl + 1)

    def walk(acc, item):
        key, node = item
        status = model.get_status(node)
        match status:
            case model.CHANGED:
                removed_value = model.get_removed(node)
                stringified_value = stringify(removed_value, lvl + 1)
                line = form_line(indent, model.REMOVED, key, stringified_value)
                acc.append(line)

                added_value = model.get_added(node)
                stringified_value = stringify(added_value, lvl + 1)
                line = form_line(indent, model.ADDED, key, stringified_value)
                acc.append(line)
            case model.NESTED:
                stringified_value = stylish(node, lvl + 1)
                line = form_line(indent, status, key, stringified_value)
                acc.append(line)
            case _:
                stringified_value = stringify(model.get_value(node), lvl + 1)
                line = form_line(indent, status, key, stringified_value)
                acc.append(line)
        return acc

    children = model.get_children(diff)
    cur_lvl = reduce(walk, sorted(children.items()), list())
    indent -= INDENT_SIZE
    result = chain('{', cur_lvl, ['}'.rjust(indent + 1)])
    return '\n'.join(result)


def stringify(node, lvl=0):
    if node is None:
        return 'null'
    elif isinstance(node, bool):
        return str(node).lower()
    elif not isinstance(node, dict):
        return str(node)

    indent = INDENT_SIZE * (lvl + 1)

    def walk(acc, item):
        key, value = item
        stringified_value = stringify(value, lvl + 1)
        line = form_line(indent, None, key, stringified_value)
        acc.append(line)
        return acc

    cur_lvl = reduce(walk, sorted(node.items()), list())
    indent -= INDENT_SIZE
    result = chain('{', cur_lvl, ['}'.rjust(indent + 1)])
    return '\n'.join(result)


def form_line(indent, status, key, value):
    sign, color = STATUSES.get(status, (' ', None))
    formatted_indent = f'{sign} '.rjust(indent)
    line = f'{formatted_indent}{key}: {value}'
    if color:
        return colored(line, color)
    return line


def plain(diff):
    pass


def json_(diff):
    pass
