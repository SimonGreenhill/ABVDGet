#!/usr/bin/env python3
#coding=utf-8
import sys
import argparse

from .ABVD import DATABASES, Downloader
from . import __version__

def parse_args(args):
    """
    Parses command line arguments

    Returns a tuple of (inputfile, method, outputfile)
    """
    parser = argparse.ArgumentParser(description='Downloads data from the ABVD')
    parser.add_argument('--version', action='version', version='%s' % __version__)
    parser.add_argument("database", help="database", choices=DATABASES)
    parser.add_argument("language", help="language", type=int)
    parser.add_argument(
        '-o', "--output", dest='output', default=None,
        help="output file", action='store'
    )
    args = parser.parse_args(args)
    return (args.database, args.language, args.output)


def main(args=None):  # pragma: no cover
    if args is None:
        args = sys.argv[1:]
    database, language, outfile = parse_args(args)
    
    d = Downloader(database)
    d.get(language)
    if outfile:
        d.write(outfile)
    else:
        print(d.data)
