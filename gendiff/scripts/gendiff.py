#! /usr/bin/env python3

"""

This module starts gendiff tool

"""

from gendiff import parser
from gendiff import generate_diff


def main():
    print("Start gendiff")
    args = parser.parse()
    first_path = args.first_file
    second_path = args.second_file
    diff = generate_diff(first_path, second_path)
    print(diff)


if __name__ == '__main__':
    main()
