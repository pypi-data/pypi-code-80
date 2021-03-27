#!/usr/bin/env python3

import logging
import textwrap
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from json import dumps
from pprint import pprint

from csirtgsdk import risk, get_feed, create_indicator

logger = logging.getLogger(__name__)


def get():  # pragma: no cover
    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ csirtg 1.1.1.1
            $ csirtg csirtgadgets/ssh-scanners
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg',
    )

    p.add_argument('q', help='search for indicator or feed')
    p.add_argument('-v', '--verbose', help='search in verbose mode',
                   action='store_true', default=False)

    args = p.parse_args()

    if '/' in args.q:
        data = get_feed(args.q)
    else:
        data = risk(args.q, args.verbose)

    print(dumps(data, indent=4))


def create():  # pragma: no cover
    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ csirtg-create 1.1.1.1 --tags scanner
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg',
    )

    p.add_argument('i', help='indicator to create')
    p.add_argument('--tags', required=True)
    p.add_argument('--confidence', type=int, default=3)
    p.add_argument('--description', help='description', required=True)
    p.add_argument('--feed', help='feed name (eg: csirtgadgets/ssh-scannerss',
                   required=True)

    args = p.parse_args()

    resp = create_indicator(args.feed, args.i, args.tags, args.description)

    pprint(resp)


if __name__ == "__main__":
    get()
