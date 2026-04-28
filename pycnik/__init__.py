#!/usr/bin/python
# -*- encoding=utf-8 -*-
import argparse
import sys

__version__ = '2.0.0'


def main():
    from .pycnik import translate, import_style

    parser = argparse.ArgumentParser(
        description="Translate Python code to Mapnik XML stylesheet or to Mapbox JSON stylesheet"
    )

    parser.add_argument('stylesheet', help='Python Stylesheet file')
    parser.add_argument('-o', '--output-file', help='File to be written')
    parser.add_argument('-k', '--mapnik', help='Output file will Mapnik XML')
    parser.add_argument('-x', '--mapbox', help='Output file will Mapbox JSON')

    mapbox = False

    args = parser.parse_args()

    source = import_style(args.stylesheet)

    if args.mapbox :
        mapbox = True

    if not args.output_file:
        result = translate(source, mapbox=mapbox)
        if isinstance(result, bytes):
            sys.stdout.buffer.write(result)
        else:
            print(result)
    else:
        translate(source, output_file=args.output_file, mapbox=mapbox)
