"""

This module implements data collection from files or network resources.

"""

import os

import requests


def fetch(path: str) -> tuple[str, str]:
    """Returns a tuple with raw data from a source and its format."""
    raw_data, data_format = None, None
    if path.startswith(('http://', 'https://')):
        raw_data = requests.get(path).text
        data_format = 'json'
    elif os.path.isfile(path):
        with open(path, 'r') as f:
            raw_data = f.read()
        if path.endswith(('yaml', 'yml')):
            data_format = 'yaml'
        if path.endswith('json'):
            data_format = 'json'
    return raw_data, data_format
