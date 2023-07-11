import os
import pytest

from gendiff import generate_diff


FORMATTED_FILE = 'stylish_format.txt'


@pytest.fixture
def expected_plain_formatted_diff(expected_plain):
    with open(os.path.join(expected_plain, FORMATTED_FILE)) as f:
        expected_data = f.read()
    return expected_data


@pytest.fixture
def expected_nested_formatted_diff(expected_nested):
    with open(os.path.join(expected_nested, FORMATTED_FILE)) as f:
        expected_data = f.read()
    return expected_data


def test_generate_diff_plain(plain_cases, expected_plain_formatted_diff):
    for path1, path2 in plain_cases:
        formatted_diff = generate_diff(path1, path2, 'stylish')
        assert formatted_diff == expected_plain_formatted_diff


def test_generate_diff_nested(nested_cases, expected_nested_formatted_diff):
    for path1, path2 in nested_cases:
        formatted_diff = generate_diff(path1, path2, 'stylish')
        assert formatted_diff == expected_nested_formatted_diff
