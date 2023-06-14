import argparse


def parse():
    parser = argparse.ArgumentParser(
            prog='gendiff',
            description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', help='.yml | .yaml | .json file')
    parser.add_argument('second_file', help='.yml | .yaml | .json file')
    args = parser.parse_args()
    print(f'first file: {args.first_file}, second file: {args.second_file}')
