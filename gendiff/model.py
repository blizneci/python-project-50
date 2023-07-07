"""

This module implements a diff model.

"""

from functools import reduce, wraps

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
        An object as a function, that contains status and value.
        To get the status and value use functions below:
        'get_status(node)' returns status of the node.
        'get_value(node)' returns a value.
    """
    @wraps(make_)
    def inner(message):
        """Returns status and value."""
        match message:
            case 'get_status':
                return status
            case 'get_value':
                return value
    return inner


def make_unchanged(value):
    """Returns a diff node with status 'unchanged'."""
    return make_(UNCHANGED, value)


def make_removed(value):
    """Returns a diff node with status 'removed'."""
    return make_(REMOVED, value)


def make_added(value):
    """Returns a diff node with status 'added'."""
    return make_(ADDED, value)


def make_changed(removed_value, added_value):
    """Makes a diff node with status 'chaanged' and two values.

    Args:
        removed_value: Removed value.
        added_value: Added value.

    Returns:
        An object as a function, that contains status and changed values.
        To get the status and values use functions below:
        'get_status(node)' returns status of the node.
        'get_removed(node)' returns removed value.
        'get_added(node)' returns added value.
    """
    @wraps(make_changed)
    def inner(message):
        match message:
            case 'get_status':
                return CHANGED
            case 'get_removed':
                return removed_value
            case 'get_added':
                return added_value
    return inner


def make_nested(children):
    """Makes a nested diff node with status 'nested' and children as a dict.

    Args:
        children: A dictionary with nested diff nodes.

    Returns:
        An object as a function, that contains status and children.
        To get the status and children use functions below:
        'get_status(node)' returns status of the node.
        'get_children(node)' returns children of the nested node.
    """
    @wraps(make_nested)
    def inner(message):
        match message:
            case 'get_children':
                return children
            case 'get_status':
                return NESTED
    return inner


def get_children(node):
    """Returns children of a given nested diff node."""
    return node('get_children')


def get_value(node):
    """Returns a value of the given diff node."""
    return node('get_value')


def get_removed(node):
    """Returns removed value of the given diff node with 'changed' status."""
    return node('get_removed')


def get_added(node):
    """Returns added value of the given diff node with 'changed' status."""
    return node('get_added')


def get_status(node):
    """Returns status of the given node."""
    return node('get_status')


def is_diff(data: any):
    """Returns True if given data is a diff view, otherwise returns False."""
    return hasattr(data, '__wrapped__')


def to_dict(node):
    """Returns diff view as a dictionary."""
    status = get_status(node)
    match status:
        case 'changed':
            return {
                    'status': status,
                    'removed_value': get_removed(node),
                    'added_value': get_removed(node),
                    }
        case 'added' | 'removed' | 'unchanged':
            return {'status': status, 'value': get_value(node)}

    def walk(acc, item):
        key, value = item
        acc[key] = to_dict(value)
        return acc

    children = reduce(walk, get_children(node).items(), dict())
    return {'status': status, 'children': children}


def get_nodes_by_key(diff, target_key):
    """Returns a list of nodes in diff by key if key presents in diff."""
    def walk(acc, item):
        key, node = item
        if key == target_key:
            acc.append(item)
        if get_status(node) == NESTED:
            acc = reduce(walk, get_children(node).items(), acc)
        return acc

    return reduce(walk, get_children(diff).items(), list())
