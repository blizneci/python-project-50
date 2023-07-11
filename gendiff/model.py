"""

This module implements a diff model.

"""

from functools import reduce, wraps

ADDED = 'added'
REMOVED = 'removed'
CHANGED = 'changed'
UNCHANGED = 'unchanged'
NESTED = 'nested'


def make_(status, *, value=None, removed=None, added=None, children=None):
    """Makes a diff node with given status and value.

    Args:
        status: A status that represents what happened with the given value.
            Possible statuses are:
            'unchanged', 'added', 'removed', 'changed', 'nested'.
        value: Value of an unchanged node.
        removed: Removed value of a changed node.
        added: Added value of a changed node.
        children: children of a nested node.

    Returns:
        A callable object, that returns status, values and children.
        To get the status, values and children use functions below:
        'get_status(node)' returns a status of the node.
        'get_value(node)' returns a value of the node.
        'get_removed(node)' returns a removed value of the changed node.
        'get_added(node)' returns an added value of the changed node.
        'get_children(node)' returns children of the given nested node.
    """
    @wraps(make_)
    def inner(message):
        """Returns status and value."""
        match message:
            case 'get_status':
                return status
            case 'get_value':
                return value
            case 'get_removed':
                return removed
            case 'get_added':
                return added
            case 'get_children':
                return children
    return inner


def make_added(value):
    """Returns a diff node with status 'added'."""
    return make_(ADDED, value=value)


def make_changed(removed_value, added_value):
    """Return a changed diff node."""
    return make_(CHANGED, removed=removed_value, added=added_value)


def make_nested(children):
    """Return a nested diff node."""
    return make_(NESTED, children=children)


def make_removed(value):
    """Returns a diff node with status 'removed'."""
    return make_(REMOVED, value=value)


def make_unchanged(value):
    """Returns a diff node with status 'unchanged'."""
    return make_(UNCHANGED, value=value)


def get_added(node):
    """Returns added value of the given diff node with 'changed' status."""
    return node('get_added')


def get_children(node):
    """Returns children of a given nested diff node."""
    return node('get_children')


def get_removed(node):
    """Returns removed value of the given diff node with 'changed' status."""
    return node('get_removed')


def get_status(node):
    """Returns status of the given node."""
    return node('get_status')


def get_value(node):
    """Returns a value of the given diff node."""
    return node('get_value')


def get_nodes_by_key(diff, target_key):
    """Returns a list of nodes with target_key if it presents in diff."""
    def walk(acc, item):
        key, node = item
        if key == target_key:
            acc.append(item)
        if get_status(node) == NESTED:
            acc = reduce(walk, get_children(node).items(), acc)
        return acc

    return reduce(walk, get_children(diff).items(), list())


def is_diff(data: any):
    """Returns True if given data is a diff view, otherwise returns False."""
    return hasattr(data, '__wrapped__') and data.__name__ == 'make_'


def to_dict(node):
    """Returns diff view as a dictionary."""
    status = get_status(node)
    if status == CHANGED:
        return {
                'status': status,
                'removed': get_removed(node),
                'added': get_added(node),
                }
    if status in (ADDED, REMOVED, UNCHANGED):
        return {'status': status, 'value': get_value(node)}

    def walk(acc, item):
        key, value = item
        acc[key] = to_dict(value)
        return acc

    children = reduce(walk, get_children(node).items(), dict())
    return {'status': status, 'children': children}
