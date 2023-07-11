import os

import pytest

PLAIN_FILES = 'tests/fixtures/plain'
NESTED_FILES = 'tests/fixtures/nested'


@pytest.fixture
def plain_cases():
    return [
        (
            os.path.join(PLAIN_FILES, 'file1.json'),
            os.path.join(PLAIN_FILES, 'file2.json'),
        ),
        (
            os.path.join(PLAIN_FILES, 'file1.yaml'),
            os.path.join(PLAIN_FILES, 'file2.yml'),
        ),
    ]


@pytest.fixture
def nested_cases():
    return [
        (
            os.path.join(NESTED_FILES, 'file1.json'),
            os.path.join(NESTED_FILES, 'file2.json'),
        ),
        (
            os.path.join(NESTED_FILES, 'file1.yaml'),
            os.path.join(NESTED_FILES, 'file2.yml'),
        ),
    ]


@pytest.fixture
def expected_plain():
    return os.path.join(PLAIN_FILES, 'expected')


@pytest.fixture
def expected_nested():
    return os.path.join(NESTED_FILES, 'expected')
