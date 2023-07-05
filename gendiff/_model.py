def make_(status, value1, value2=None):
    def inner(message):
        match message:
            case 'get_status':
                return status
            case 'get_value':
                return value1
    return inner


def make_unchanged(value):
    return make_('unchanged', value)


def make_removed(value):
    return make_('removed', value)


def make_added(value):
    return make_('added', value)


def make_changed(value1, value2):
    def inner(message):
        match message:
            case 'get_status':
                return 'changed'
            case 'get_removed':
                return 'removed', value1
            case 'get_added':
                return 'added', value2
    return inner


def make_nested():
    children = dict()

    def inner(message, key=None, child_node=None):
        match message:
            case 'set_child':
                children[key] = child_node
            case 'get_children':
                return children
            case 'get_status':
                return 'nested'
    return inner


def set_child(nested_node, key, child_node):
    nested_node('set_child', key, child_node)


def get_children(node):
    if isinstance(node, dict):
        return node
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


def is_diff(data):
    return hasattr(data, '__call__')


def to_dict(node):
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
    children = get_children(diff)
    for child in children:
        node = children.get(child)
        if child == key:
            return node
        if is_nested(node):
            new_node = get_node_by_key(node, key)
            if new_node:
                return new_node
