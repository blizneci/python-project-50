import argparse


def parse():
    """Returns arguments, parsed from command line."""
    parser = argparse.ArgumentParser(
        prog='gendiff',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Compares two configuration files and shows a differense.',
        usage='gendiff [options] <filepath1> <filepath2>',
    )
    parser.add_argument(
        '-f', '--format',
        dest='FORMAT',
        choices=['stylish', 'plain', 'json'],
        metavar='[type]',
        default='stylish',
        help='set format of output',
    )
    parser.add_argument('first_file', help=argparse.SUPPRESS)
    parser.add_argument('second_file', help=argparse.SUPPRESS)
    parser._optionals.title = 'Options'
    return parser.parse_args()
