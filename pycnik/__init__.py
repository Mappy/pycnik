#!/usr/bin/python
# -*- encoding=utf-8 -*-
import argparse

__version__ = '1.3.2.1'


def main():
    from .pycnik import translate, import_style

    parser = argparse.ArgumentParser(
        description="Translate Python code to Mapnik XML stylesheet"
    )

    parser.add_argument('stylesheet', help='Python Stylesheet file')
    parser.add_argument('-o', '--output-file', help='XML file to be written')

    args = parser.parse_args()

    source = import_style(args.stylesheet)

    if not args.output_file:
        print(translate(source))
    else:
        translate(source, output_file=args.output_file)
