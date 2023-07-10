from gendiff.formatters import json_formatter, plain, stylish


def get_formatter(output_format):
    match output_format:
        case 'stylish':
            return stylish
        case 'plain':
            return plain
        case 'json':
            return json_formatter


all = (
        'get_formatter',
        )
