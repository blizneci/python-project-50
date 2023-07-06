"""

This module implements diff model.

"""

from functools import wraps

ADDED = 'added'
REMOVED = 'removed'
CHANGED = 'changed'
UNCHANGED = 'unchanged'
NESTED = 'nested'


def make_(status, value):
    """Makes a diff node with given status and value.

    Args:
        status: A status than represents what happened with the given value.
            Possible statuses are: 'unchanged', 'added', 'removed'.
        value: Any type of value.

    Returns:
        A function, that returns status or value according to given message.
        For example:
        'get_status(node)' return status of the node.
        'get_value(node)' returns a value of the node.
    """
    @wraps(make_)
    def inner(message):
        match message:
            case 'get_status':
                return status
            case 'get_value':
                return value
    return inner


def make_unchanged(value):
    return make_(UNCHANGED, value)


def make_removed(value):
    return make_(REMOVED, value)


def make_added(value):
    return make_(ADDED, value)


def make_changed(value1, value2):
    @wraps(make_changed)
    def inner(message):
        match message:
            case 'get_status':
                return CHANGED
            case 'get_removed':
                return value1
            case 'get_added':
                return value2
    return inner


def make_nested():
    """Returns diff view with empty children dict, without value."""
    children = dict()

    @wraps(make_nested)
    def inner(message, key=None, child_node=None):
        match message:
            case 'set_child':
                children[key] = child_node
            case 'get_children':
                return children
            case 'get_status':
                return NESTED
    return inner


def set_child(nested_node, key, child_node):
    nested_node('set_child', key, child_node)


def get_children(node):
    return node('get_children')


def get_value(node):
    return node('get_value')


def get_removed(node):
    return node('get_removed')


def get_added(node):
    return node('get_added')


def get_status(node):
    return node('get_status')


def is_nested(node):
    return get_status(node) == 'nested'


def is_changed(node):
    return get_status(node) == 'changed'


def is_diff(data: any):
    """Returns True if given data is a diff view, otherwise returns False."""
    return hasattr(data, '__call__')


def to_dict(node):
    """Returns diff view as a dictionary."""
    if not is_nested(node):
        if is_changed(node):
            status = get_status(node)
            _, removed_value = get_removed(node)
            _, added_value = get_added(node)
            return {
                    'status': status,
                    'removed_value': removed_value,
                    'added_value': added_value
                    }
        else:
            return {'status': get_status(node), 'value': get_value(node)}
    dict_node = dict()
    dict_node['children'] = dict()
    dict_node['status'] = get_status(node)
    children = get_children(node)
    for key, node in children.items():
        dict_node['children'][key] = to_dict(node)

    return dict_node


def get_node_by_key(diff, key):
    """Returns a node in diff for given key, if key is presents in diff."""
    children = get_children(diff)
    for child in children:
        node = children.get(child)
        if child == key:
            return node
        if is_nested(node):
            new_node = get_node_by_key(node, key)
            if new_node:
                return new_node
