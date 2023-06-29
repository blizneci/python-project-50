#! /usr/bin/env python3

"""

This module starts gendiff tool

"""

from gendiff import cli
from gendiff.gendiff import gen_diff
from gendiff.parser import parse
from gendiff.formatter import format_output


def main():
    args = cli.parse()
    first_file_path = args.first_file
    second_file_path = args.second_file
    output_format = args.FORMAT
    first_file_data = parse(first_file_path)
    second_file_data = parse(second_file_path)
    diff = gen_diff(first_file_data, second_file_data)
    format_output(diff, output_format)


if __name__ == '__main__':
    main()
