def make_nested(data1, data2):
    all_keys = data1.keys() | data2.keys()
    node = dict()
    node['status'] = 'nested'
    node['children'] = dict.fromkeys(all_keys, None)
    return node


def make_node(status, value):
    return {'status': status, 'value': value}

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


def set_added(node, key, value):
    added_node = make_node('added', value)
    node['children'][key] = added_node

def set_deleted(node, key, value):
    deleted_node = make_node('deleted', value)
    node['children'][key] = deleted_node

def set_common(node, key, value):
    common_node = value
    node['children'][key] = common_node

def get_children(node):
    return sorted(node['children'].keys())
