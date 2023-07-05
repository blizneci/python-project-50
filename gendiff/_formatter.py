from itertools import chain

from termcolor import colored

from gendiff._model import is_diff, is_changed, is_nested
from gendiff._model import get_children, get_status
from gendiff._model import get_added, get_removed, get_value


INDENT_SIZE = 4
STATUSES = {
        'added': ('+', 'green'),
        'removed': ('-', 'red'),
        }


def form_line(indent, status, key, value):
    sign, color = STATUSES.get(status, (' ', None))
    formatted_indent = f'{sign} '.rjust(indent)
    line = f'{formatted_indent}{key}: {value}'
    if color:
        return colored(line, color)
    return line


def stylish(diff):
    def stringify(diff, lvl=0):
        if diff is None:
            return 'null'
        elif isinstance(diff, bool):
            return str(diff).lower()
        elif not (isinstance(diff, dict) or is_diff(diff)):
            return str(diff)

        indent = INDENT_SIZE * (lvl + 1)
        cur_lvl = list()
        children = get_children(diff)
        for key, node in sorted(children.items()):
            if isinstance(diff, dict):
                stringified_value = stringify(node, lvl + 1)
                status = None
                line = form_line(indent, status, key, stringified_value)
                cur_lvl.append(line)
                continue
            if is_changed(node):
                status, removed_value = get_removed(node)
                stringified_value = stringify(removed_value, lvl + 1)
                line = form_line(indent, status, key, stringified_value)
                cur_lvl.append(line)

                status, added_value = get_added(node)
                stringified_value = stringify(added_value, lvl + 1)
                line = form_line(indent, status, key, stringified_value)
                cur_lvl.append(line)
            elif is_nested(node):
                status = get_status(node)
                stringified_value = stringify(node, lvl + 1)
                line = form_line(indent, status, key, stringified_value)
                cur_lvl.append(line)
            else:
                status = get_status(node)
                stringified_value = stringify(get_value(node), lvl + 1)
                line = form_line(indent, status, key, stringified_value)
                cur_lvl.append(line)

        indent -= INDENT_SIZE
        result = chain('{', cur_lvl, ['}'.rjust(indent + 1)])
        return '\n'.join(result)

    return stringify(diff)
