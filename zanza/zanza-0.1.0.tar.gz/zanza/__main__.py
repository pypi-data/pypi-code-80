#!/usr/bin/env python

import argparse
import json
import logging

from . import zanza, __doc__ as manual

logger = logging.getLogger(__name__)

def main():
    """Obfuscator main program.
    """

    parser = argparse.ArgumentParser(
        description="Obfuscate the given input string",
        epilog=manual,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="Input string to obfuscate")
    args = parser.parse_args()

    try:
        z = zanza(args.source)
        zj = json.dumps(z)
        print(zj)
    except Exception as ex:
        logger.error("ERROR: %s" % ex)


if __name__ == "__main__":
    main()
