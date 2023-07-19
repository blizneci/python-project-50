import os
from itertools import chain, cycle, product, repeat

import pytest

from gendiff import generate_diff


EXPECTED_FILES = (
    'expected/plain_format.txt',
    'expected/stylish_format.txt',
    'expected/json_format.txt',
)
FIRST_FILE_NAMES = ('file1.json', 'file1.yaml')
FIXTURES_PATHS = ('tests/fixtures/plain', 'tests/fixtures/nested')
FORMATS = ('plain', 'stylish', 'json')
SECOND_FILE_NAMES = ('file2.json', 'file2.yml')


def get_paths(files):
    path_parts = product(FIXTURES_PATHS, files)
    paths = map(lambda parts: os.path.join(*parts), path_parts)
    for path in paths:
        yield from repeat(path, 3)


def get_expected_paths():
    path_parts = product(FIXTURES_PATHS, chain(*repeat(EXPECTED_FILES, 2)))
    paths = map(lambda parts: os.path.join(*parts), path_parts)
    yield from paths


def idfn(val):
    if 'file2' in val or val in FORMATS:
        return ''
    path, sep, file_name = val.rpartition('/')
    if 'expected' in path:
        if 'plain' in path:
            return f'plain--{file_name.removesuffix(".txt")}'
        return f'nested--{file_name.removesuffix(".txt")}'
    file_type = file_name.rpartition('.')[-1]
    return file_type


@pytest.mark.parametrize(
    'path1, path2, format_, expected',
    list(zip(
        get_paths(FIRST_FILE_NAMES),
        get_paths(SECOND_FILE_NAMES),
        cycle(FORMATS),
        get_expected_paths(),
    )),
    ids=idfn,
)
def test_generate_diff(path1, path2, format_, expected):
    with open(expected, 'r') as f:
        expected_formatted_diff = f.read()
    assert generate_diff(path1, path2, format_) == expected_formatted_diff
