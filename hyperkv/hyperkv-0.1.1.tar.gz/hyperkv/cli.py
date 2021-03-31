"""
Surprisingly, this module implements an interface of the command line variety.
"""

from .reader import read_kv_from_file

import argparse
import json
import sys
from .__version__ import __version__


def command_line():
    """
    Handle user input from the command line and output the result to JSON

    :return:
    """
    parser = argparse.ArgumentParser("hyperkv")
    parser.add_argument("-e", "--encoding", default="utf-8",
                        help="The expected encoding of the values in Hyper-V KV")
    parser.add_argument("-f", "--file", default="/var/lib/hyperv/.kvp_pool_3",
                        help="The path to a .kvp_pool_* file to read values from.",
                        dest="filepath")
    parser.add_argument("-v", "-V", "--version", action="store_true",
                        help="Print the version and quit. Spoiler alert it's 'hyperkv v%s'." % __version__,
                        dest="version")

    args = parser.parse_args()
    if args.version:
        print("hyperkv v%s" % __version__)
        return
    kv = read_kv_from_file(args.filepath, args.encoding)
    output = json.dumps(kv, indent=2)  # write our key/value pairs to standard out as a JSON dictionary
    print(output)
