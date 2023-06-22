import pytest

import json, os
from gendiff import generate_diff
from gendiff.gendiff import gen_diff, stringify


@pytest.fixture
def path1():
    path = 'file10.json'
    data = {
            "host": "hexlet.io",
            "timeout": 50,
            "proxy": "123.234.53.22",
            "follow": False,
            }
    json.dump(data, open(path, 'w'))
    yield path
    os.remove(path)


@pytest.fixture
def path2():
    path = 'file20.json'
    data = {
            "host": "hexlet.io",
            "timeout": 20,
            "verbose": True,
            }
    json.dump(data, open(path, 'w'))
    yield path
    os.remove(path)


@pytest.fixture
def not_exist_path():
    path = 'not_exist.json'
    open(path, 'w')
    os.remove(path)
    return path

def test_existence(path1, path2, not_exist_path):
    assert os.path.exists(path1)
    assert os.path.exists(path2)
    assert not os.path.exists(not_exist_path)


def test_gen_diff(path1, path2):
    expected = {
            "host": "unchanged",
            "follow": "deleted",
            "proxy": "deleted",
            "timeout": "changed",
            "verbose": "added",
            }
    data1 = json.load(open(path1))
    data2 = json.load(open(path2))
    assert gen_diff(data1, data2) == expected


def test_generate_diff(path1, path2):
    expected = '{\n  - follow: false\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}'
    assert generate_diff(path1, path2) == expected


def test_generate_diff_not_exist(path1, not_exist_path):
    assert not generate_diff(path1, not_exist_path)
