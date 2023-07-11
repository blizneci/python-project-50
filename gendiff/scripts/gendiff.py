#! /usr/bin/env python3

"""

This module starts gendiff tool

"""

from gendiff import cli, generate_diff


def main():
    args = cli.parse()
    first_file_path = args.first_file
    second_file_path = args.second_file
    format_ = args.FORMAT
    output = generate_diff(first_file_path, second_file_path, format_)
    print(output)


if __name__ == '__main__':
    main()
