import os
from itertools import cycle, repeat, chain

import pytest

from gendiff import generate_diff


FIXTURES_PATHS = ('tests/fixtures/plain', 'tests/fixtures/nested')
EXPECTED_FILES = ('plain_format.txt', 'stylish_format.txt', 'json_format.txt')
FORMATS = ('plain', 'stylish', 'json')
FIRST_FILE_NAMES = ('file1.json', 'file1.yaml')
SECOND_FILE_NAMES = ('file2.json', 'file2.yml')


def get_path(files):
    for fixture_path in FIXTURES_PATHS:
        for file_name in files:
            path = os.path.join(fixture_path, file_name)
            yield from repeat(path, 3)


def get_expected():
    for fixture_path in FIXTURES_PATHS:
        for file_name in chain(*repeat(EXPECTED_FILES, 2)):
            path = os.path.join(fixture_path, 'expected', file_name)
            yield path


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
        get_path(FIRST_FILE_NAMES),
        get_path(SECOND_FILE_NAMES),
        cycle(FORMATS),
        get_expected(),
    )),
    ids=idfn,
)
def test_generate_diff(path1, path2, format_, expected):
    with open(expected, 'r') as f:
        expected_formatted_diff = f.read()
    assert generate_diff(path1, path2, format_) == expected_formatted_diff
