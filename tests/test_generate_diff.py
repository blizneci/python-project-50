import pytest

from gendiff import generate_diff


path1_plain = 'tests/fixtures/plain/file1.json'
path2_plain = 'tests/fixtures/plain/file2.json'
expected_plain = 'tests/fixtures/plain/expected.txt'


def test_generate_diff_plain_json():
    expected_data = open(expected_plain).read()
    print(expected_data)
    print(generate_diff(path1_plain, path2_plain))
    assert generate_diff(path1_plain, path2_plain) == expected_data
