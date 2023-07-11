import argparse


def parse():
    """Returns arguments, parsed from command line."""
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a differense.',
    )
    parser.add_argument(
        '-f, --format',
        dest='FORMAT',
        default='stylish',
        help='set format of output',
    )
    parser.add_argument('first_file', help='.yml | .yaml | .json file')
    parser.add_argument('second_file', help='.yml | .yaml | .json file')
    return parser.parse_args()
