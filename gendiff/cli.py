import argparse


def parse():
    parser = argparse.ArgumentParser(
            prog='gendiff',
            description='Compares two configuration files \
            and shows a difference.')
    parser.add_argument(
            '-f', '--format',
            dest='FORMAT',
            default='plain',
            help='set format of output')
    parser.add_argument('first_file', help='.yml | .yaml | .json file')
    parser.add_argument('second_file', help='.yml | .yaml | .json file')
    args = parser.parse_args()
    return args