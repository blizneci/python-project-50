"""

This module implements parser for data in json or yaml | yml formats.

"""

import json

import yaml
from yaml.resolver import Resolver

resolvers = Resolver.yaml_implicit_resolvers

for ch in 'Oo':
    if len(resolvers[ch]) == 1:
        del resolvers[ch]
    else:
        tag = 'tag:yaml.org, 2002:bool'
        resolvers[ch] = [x for x in resolvers[ch] if x[0] != tag]


def parse(data: str, data_format: str) -> dict | list:
    """Returns data in json or yaml format as a dictionary."""
    if data_format == 'json':
        return json.loads(data)
    if data_format == 'yaml':
        return yaml.load(data, Loader=yaml.Loader)
