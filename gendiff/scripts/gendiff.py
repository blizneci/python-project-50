#! /usr/bin/env python3

"""

This module starts gendiff tool

"""

from gendiff import parser


def main():
    print("Start gendiff")
    args = parser.parse()
    print(args)


if __name__ == '__main__':
    main()
