from itertools import chain
frum functools import reduce

from termcolor import colored

from gendiff._model import get_, walk


INDENT_SIZE = 4
STATUSES = {
        'added': ('+ ', 'green'),
        'removed': ('- ', 'red'),
        None: ('  ', None),
        }

def stylish(diff):

    def walk(node, lvl=0):
        if not is_nested(node):
            return get_value(node)

        children = get_children(node)
        indent = INDENT_SIZE * (lvl + 1)
        cur_level = list()

        for key, cur_node in sorted(children.items()):
            if is_changed(node):
                sign, color = get_sign_color('removed')
                removed_value = get_removed_value(cur_node)
                removed_line = form_line(key, removed_value)
                sign, color = get_sign_color('added')
                added_value = get_added_value(cur_node)
                added_line = form_line(...)
            else:
                value = walk(cur_node, lvl + 1)







