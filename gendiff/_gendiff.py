from _model import *


def gen_diff(data1, data2):
    if is_nested(data1, data2):
        node = make_nested(data1, data2)
        
        for key in get_children(node):
            value1 = data1.get(key)
            value2 = data2.get(key)
            if key not in data1:
                set_added(node, key, value2)
            elif key not in data2:
                set_deleted(node, key, value1)
            else:
                set_common(node, key, gen_diff(value1, value2))

        return node

    if data1 != data2:
        return make_changed(data1, data2)
    else:
        return make_unchanged(data1, data2)

def is_nested(data1, data):
    return isinstance(data1, dict) and isinstance(data2, dict)

import os, json
f1 = '../tests/fixtures/nested/file1.json'
f2 = '../tests/fixtures/nested/file2.json'
data1 = json.load(open(f1))
data2 = json.load(open(f2))

