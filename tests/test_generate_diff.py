import pytest

from gendiff import generate_diff
from termcolor import colored


PATH1_PLAIN = 'tests/fixtures/plain/file1.json'
PATH2_PLAIN = 'tests/fixtures/plain/file2.json'
EXPECTED_PLAIN = 'tests/fixtures/plain/expected.txt'

PATH1_NESTED = 'tests/fixtures/nested/file1.json'
PATH2_NESTED = 'tests/fixtures/nested/file2.json'
EXPECTED_NESTED = 'tests/fixtures/nested/expected.txt'


def test_generate_diff_plain_json():
    expected_data = open(EXPECTED_PLAIN).read()
    diff = generate_diff(PATH1_PLAIN, PATH2_PLAIN)
    assert diff == expected_data


def test_generate_diff_nested_json():
    expected_data = open(EXPECTED_NESTED).read()
    diff = generate_diff(PATH1_NESTED, PATH2_NESTED)
    assert diff == expected_data

