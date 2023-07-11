"""

This module implements parser for json and yaml | yml files.

"""

import json
import yaml
from yaml import Loader
from yaml.resolver import Resolver


resolvers = Resolver.yaml_implicit_resolvers

for ch in "Oo":
    if len(resolvers[ch]) == 1:
        del resolvers[ch]
    else:
        tag = 'tag:yaml.org, 2002:bool'
        resolvers[ch] = [x for x in resolvers[ch] if x[0] != tag]


def parse(path: str) -> dict | list:
    """Reads data from the file and returns it as a dictionary."""
    if path.endswith(('.yaml', '.yml')):
        return yaml.load(open(path, 'r'), Loader=Loader)
    return json.load(open(path, 'r'))
