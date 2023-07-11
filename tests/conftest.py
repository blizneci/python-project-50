import os
import pytest

FIXTURES_PATH = 'tests/fixtures'
PLAIN_FILES= os.path.join(FIXTURES_PATH, 'plain')
EXPECTED_PLAIN_FILES = os.path.join(PLAIN_FILES, 'expected')
NESTED_FILES= os.path.join(FIXTURES_PATH, 'nested')
EXPECTED_NESTED_FILES = os.path.join(NESTED_FILES, 'expected')

PLAIN_CASES = [
        (
            os.path.join(PLAIN_FILES, 'file1.json'),
            os.path.join(PLAIN_FILES, 'file2.json'),
        ),
        (
            os.path.join(PLAIN_FILES, 'file1.yaml'),
            os.path.join(PLAIN_FILES, 'file2.yml')
        ),
        ]

NESTED_CASES = [
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
def plain_cases():
    return PLAIN_CASES


@pytest.fixture
def nested_cases():
    return NESTED_CASES


@pytest.fixture
def expected_plain():
    return EXPECTED_PLAIN_FILES


@pytest.fixture
def expected_nested():
    return EXPECTED_NESTED_FILES
