import json

from gendiff import model


def stringify(diff):
    transformed_diff = model.to_dict(diff)
    return json.dumps(transformed_diff, sort_keys=True, indent=4)
