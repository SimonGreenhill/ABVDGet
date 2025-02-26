#!/usr/bin/env python3
#coding=utf-8
import sys
import time
import codecs
import argparse
import asyncio
from pathlib import Path

import httpx

from abvd.ABVD import URL, XMLTEMPLATE
from abvd.ABVD import DEAD_LANGUAGES

MAX_LANGUAGES = 1800
LIMITS = httpx.Limits(max_keepalive_connections=5, max_connections=10)


async def download_to_file(client, abvd_id, outputdir):
    url = URL % {'db': 'austronesian', 'id': abvd_id}
    try:
        response = await client.get(url, timeout=60)
    except Exception as e:
        return url, f"Error: {e}" 

    if len(response.text):
        with codecs.open(outputdir / ('%d.xml' % abvd_id), 'w', 'utf8') as out:
            out.write(XMLTEMPLATE % response.text)
            print('.')
            return url, response.status_code
    else:
        return url, "no content"


async def fetch_all(abvd_ids, outputdir):
    async with httpx.AsyncClient(default_encoding="utf-8", limits=LIMITS) as client:
        tasks = [download_to_file(client, abvd_id, outputdir) for abvd_id in abvd_ids]
        return await asyncio.gather(*tasks)



async def get(args=None):  # pragma: no cover

    if args.output.exists():
        downloaded = [int(f.stem) for f in args.output.glob("*.xml")] + DEAD_LANGUAGES['austronesian']
    else:
        args.output.mkdir()
        downloaded = DEAD_LANGUAGES['austronesian']

    abvd_ids = [i for i in range(args.start, args.stop) if i not in downloaded]
    print(len(abvd_ids))
    results = await fetch_all(abvd_ids, args.output)
    for url, status in results:
        print(f"{url} -> {status}")


def main(args=None):  # pragma: no cover
    parser = argparse.ArgumentParser(description='Downloads data from the ABVD in XML')
    parser.add_argument("--start", dest="start", help="start ID", type=int, default=1)
    parser.add_argument("--stop", dest="stop", help="stop ID", type=int, default=MAX_LANGUAGES)
    parser.add_argument("output", help="output", type=Path)
    if args is None:
        args = sys.argv[1:]
    args = parser.parse_args(args)
    asyncio.run(get(args))