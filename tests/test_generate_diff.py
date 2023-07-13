import os

import pytest

from gendiff import generate_diff

PLAIN_FILES_PATH = 'tests/fixtures/plain'
NESTED_FILES_PATH = 'tests/fixtures/nested'
EXPECTED_FILES_SUBDIR = 'expected'
CASE_FILES = [('file1.json', 'file2.json'), ('file1.yaml', 'file2.yml')]
EXPECTED_FILES = ['plain_format.txt', 'json_format.txt', 'stylish_format.txt']
FORMATS = ['plain', 'json', 'stylish']


@pytest.mark.parametrize('case_pair', CASE_FILES)
@pytest.mark.parametrize(
    'expected_file_name, format_',
    list(zip(EXPECTED_FILES, FORMATS)),
)
@pytest.mark.parametrize('files_path', [PLAIN_FILES_PATH, NESTED_FILES_PATH])
def test_generate_diff(files_path, case_pair, expected_file_name, format_):
    path1, path2 = map(
        lambda file_name: os.path.join(files_path, file_name),
        case_pair,
    )
    expected_diff_path = os.path.join(
        files_path,
        EXPECTED_FILES_SUBDIR,
        expected_file_name,
    )
    with open(expected_diff_path, 'r') as f:
        expected_formatted_diff = f.read()
    formatted_diff = generate_diff(path1, path2, format_)
    assert formatted_diff == expected_formatted_diff
