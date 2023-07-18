"""

This module implements parser for data in json or yaml | yml formats.

"""

import json

import yaml


def parse(data: str, data_format: str) -> dict | list:
    """Returns data in json or yaml format as a dictionary."""
    if data_format == 'json':
        return json.loads(data)
    if data_format == 'yaml':
        return yaml.load(data, Loader=yaml.Loader)
