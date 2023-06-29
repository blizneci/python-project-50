import pytest

from gendiff import generate_diff


PATH1_PLAIN = 'tests/fixtures/plain/file1.json'
PATH2_PLAIN = 'tests/fixtures/plain/file2.json'
PATH1_PLAIN_YAML = 'tests/fixtures/plain/file1.yaml'
PATH2_PLAIN_YAML = 'tests/fixtures/plain/file2.yaml'
EXPECTED_PLAIN_DIFF = 'tests/fixtures/plain/expected.txt'

PATH1_NESTED = 'tests/fixtures/nested/file1.json'
PATH2_NESTED = 'tests/fixtures/nested/file2.json'
PATH1_NESTED_YAML = 'tests/fixtures/nested/file1.yaml'
PATH2_NESTED_YAML = 'tests/fixtures/nested/file2.yaml'
EXPECTED_NESTED_DIFF = 'tests/fixtures/nested/expected.txt'


@pytest.fixture
def expected_plain_diff():
    with open(EXPECTED_PLAIN_DIFF) as f:
        expected_data = f.read()
    return expected_data


@pytest.fixture
def expected_nested_diff():
    with open(EXPECTED_NESTED_DIFF) as f:
        expected_data = f.read()
    return expected_data


def test_generate_diff_plain_json(expected_plain_diff):
    diff = generate_diff(PATH1_PLAIN, PATH2_PLAIN)
    assert diff == expected_plain_diff


def test_generate_diff_plain_yaml(expected_plain_diff):
    diff = generate_diff(PATH1_PLAIN_YAML, PATH2_PLAIN_YAML)
    assert diff == expected_plain_diff


def test_generate_diff_nested_json(expected_nested_diff):
    diff = generate_diff(PATH1_NESTED, PATH2_NESTED)
    assert diff == expected_nested_diff


def test_generate_diff_nested_yaml(expected_nested_diff):
    diff = generate_diff(PATH1_NESTED_YAML, PATH2_NESTED_YAML)
    assert diff == expected_nested_diff
