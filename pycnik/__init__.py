#!/usr/bin/python
# -*- encoding=utf-8 -*-
import argparse

def main():
    from .pycnik import translate

    parser = argparse.ArgumentParser(
        description="Translate Python code to Mapnik XML stylesheet"
    )

    parser.add_argument('stylesheet', help='Python Stylesheet file')
    parser.add_argument('-o', '--output-file', help='XML file to be written')

    args = parser.parse_args()

    if not args.output_file:
        print(translate(args.stylesheet))
    else:
        translate(args.stylesheet, output_file=args.output_file)
