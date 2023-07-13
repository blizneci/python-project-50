#! /usr/bin/env python3

"""

This module starts gendiff tool

"""

from gendiff import cli, generate_diff


def main():
    args = cli.parse()
    path1 = args.first_path
    path2 = args.second_path
    format_ = args.FORMAT
    output = generate_diff(path1, path2, format_)
    print(output)


if __name__ == '__main__':
    main()
