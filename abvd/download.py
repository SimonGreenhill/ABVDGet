#!/usr/bin/env python3
#coding=utf-8
import sys
import json
import argparse

from abvd.ABVD import DATABASES, Downloader
from abvd import __version__


def main(args=None):  # pragma: no cover
    parser = argparse.ArgumentParser(description='Downloads data from the ABVD')
    parser.add_argument('--raw', dest='raw', help="save XML", action="store_true", default=False)
    parser.add_argument("database", help="database", choices=DATABASES)
    parser.add_argument("language", help="language", type=int)
    parser.add_argument(
        '-o', "--output", dest='output', default=None,
        help="output file", action='store'
    )
    if args is None:
        args = sys.argv[1:]
    args = parser.parse_args(args)

    db = Downloader(args.database)
    content = db.get(args.language, raw=args.raw)

    if args.output:
        if args.raw:
            db.write(output, xml=content)
        else:
            db.write(output, content=content)
    else:
        if args.raw:
            print(content)
        else:
            print(json.dumps(content, sort_keys=True, indent=2, ensure_ascii=False))
