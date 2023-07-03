from _model import *


def gen_diff(data1, data2):
    if isinstance(data1, dict) and isinstance(data2, dict):
        node = make_nested()

        all_keys = data1.keys() | data2.keys()
        
        for key in all_keys:
            value1 = data1.get(key)
            value2 = data2.get(key)
            if key not in data1:
                child_node = gen_diff(value2, value2)
                set_status('added', child_node)
                # set_('added', node, key, value2)
            elif key not in data2:
                child_node = gen_diff(value1, value1)
                set_status('removed', child_node)
                # set_('removed', node, key, value1)
            else:
                child_node = gen_diff(value1, value2)
                # set_('common', node, key, gen_diff(value1, value2))
            set_child(node, key, child_node)

        return node

    if data1 != data2:
        return make_changed(data1, data2)
    else:
        return make_unchanged(data1)


import os, json
f1 = '../tests/fixtures/nested/file1.json'
f2 = '../tests/fixtures/nested/file2.json'
data1 = json.load(open(f1))
data2 = json.load(open(f2))

diff = gen_diff(data1, data2)
