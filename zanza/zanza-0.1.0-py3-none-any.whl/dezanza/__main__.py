#!/usr/bin/env python

import argparse
import json
import logging

from . import dezanza, __doc__ as manual

logger = logging.getLogger(__name__)

def main():
    """Deobfuscator main program.
    """

    parser = argparse.ArgumentParser(
        description="Deobfuscate the given input sequence",
        epilog=manual,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="JSON-encoded input sequence to deobfuscate")
    args = parser.parse_args()

    try:
        zj = json.loads(args.source)
        zs = dezanza(zj)
        print(zs)
    except Exception as ex:
        logger.error("ERROR: %s" % ex)


if __name__ == "__main__":
    main()
