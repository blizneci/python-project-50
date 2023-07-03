"""
def make_nested(data1, data2):
    node = dict()
    node['status'] = 'nested'
    node['children'] = dict()
    return node


def make_changed(data1, data2):
    changed_node = {
            'status': 'changed',
            'deleted_value': data1,
            'added_value': data2,
            }
    return changed_node


def make_unchanged(data1, data2):
    unchanged_node = make_node('unchanged', data1)
    return unchanged_node


def make_node(status, value):
    return {'status': status, 'value': value}


def set_added(node, key, value):
    added_node = make_node('added', value)
    node['children'][key] = added_node


def set_deleted(node, key, value):
    deleted_node = make_node('deleted', value)
    node['children'][key] = deleted_node


def set_(status, node, key, value):
    node = make_node(status, value)
    node['children'][key] = node


"""

def to_dict(node):
    if not is_nested(node):
        value = (get_value(node), get_removed_value(node), get_added_value(node))
        status = get_status(node)
        is_nested_flag = is_nested(node)
        return {'status': status, 'is_nested': is_nested_flag, 'value': value}
    dict_node = dict()
    dict_node['children'] = dict()
    dict_node['status'] = get_status(node)
    dict_node['is_nested'] = is_nested(node)
    children = get_children(node)
    for child in children:
        dict_node['children'][child] = to_dict(children.get(child))

    return dict_node





# def make_node(status, value1=None, value2=None):
#     node = {'status': status}
#     if status == 'changed':
#         node['removed_value'] = value1
#         node['added_value'] = value2
#     elif status == 'nested':
#         node['children'] = dict()
#     else:
#         node['value'] = value1
#     return node




def make_(status, value1=None, value2=None):
    node = {'status': status, 'is_nested': False}

    if status == 'changed':
        node['removed_value'] = value1
        node['added_value'] = value2
    else:
        node['value'] = value1

    def inner(message, *args):
        match message:
            case 'set_status':
                new_status, *_ = args
                node['status'] = new_status
            case 'get_status':
                return node.get('status')
            case 'get_value':
                return node.get('value')
            case 'get_removed_value':
                return node.get('removed_value')
            case 'get_added_value':
                return node.get('added_value')
            case 'is_nested':
                return node.get('is_nested')

    return inner



def make_nested():
    nested_node = {'status': 'common', 'is_nested': True, 'children': dict()}

    def inner(message, *args):
        match message:
            case 'set_child':
                key, child_node = args
                nested_node['children'][key] = child_node
            case 'set_status':
                new_status, *_ = args
                nested_node['status'] = new_status
            case 'get_children':
                return nested_node.get('children')
            case 'get_status':
                return nested_node.get('status')
            case 'is_nested':
                return nested_node.get('is_nested')

    return inner


def make_changed(data1, data2):
    return make_('changed', data1, data2)

def make_unchanged(data):
    return make_('unchanged', data)


# For nested nodes
def set_child(nested_node, key, child_node):
    nested_node('set_child', key, child_node)

def set_status(status, node):
    node('set_status', status)

# def set_added(node, key, value):
#     node('set_added', key, value)
# 
# def set_removed(node, key, value):
#     node('set_removed', key, value)
# 
# def set_common(node, key, value):
#     node('set_common', key, value)


# def get_(message, node):
#     match message:
#         case 'added_value':
#             return node('get_added_value')
#         case 'removed_value':
#             return node('get_removed_value')
#         case 'value':
#             return node('get_value')
#         case 'children':
#             return node('get_children')
#         case 'status':
#             return node('get_status')

def get_children(node):
    return node('get_children')

def get_value(node):
    return node('get_value')

def get_removed_value(node):
    return node('get_removed_value')

def get_added_value(node):
    return node('get_added_value')

def get_status(node):
    return node('get_status')

def is_nested(node):
    return node('is_nested')

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
