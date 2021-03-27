"""
callooktools commandline interface
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


import argparse
from dataclasses import asdict
from typing import Dict, Any
from enum import Enum
from sys import stderr
from datetime import datetime

from callooktools import CallookSync, CallookError
from callooktools.callooktools import EntryStatus

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.style import Style
except ModuleNotFoundError:
    print("To use the callooktools CLI you must install 'rich'", file=stderr)
    raise SystemExit(42)


def tabulate(d: Dict[str, Any], colour: bool = False) -> str:
    result = ""
    for field, val in d.items():
        if isinstance(val, list):
            val = "\n    " + "\n    ".join(val)
        if isinstance(val, Enum):
            val = val.value
        if isinstance(val, datetime):
            if val == datetime.min:
                val = "Unknown"
            else:
                val = val.strftime("%Y-%m-%d")
        elif isinstance(val, dict):
            if colour:
                val = "\n    " + "\n    ".join([f"[yellow]{k}:[/yellow] {v}" for k, v in val.items()])
            else:
                val = "\n    " + "\n    ".join([f"{k}: {v}" for k, v in val.items()])
        if colour:
            result += f"[blue]{field}:[/blue] [default]{val}[/default]\n"
        else:
            result += f"{field}: {val}\n"
    return result.rstrip("\n")


parser = argparse.ArgumentParser(prog="callooktools", description="Retrieve callsign data from callook.info.")
parser.add_argument("--no-pretty", required=False, action="store_false", dest="pretty",
                    help="Don't pretty-print output")
parser.add_argument("call", type=str, metavar="CALL", nargs="+", help="The callsign(s) to look up")
args = parser.parse_args()

if args.pretty:
    c = Console()
    ec = Console(stderr=True, style="bold red")


callook = CallookSync()

print()

if args.call:
    for call in args.call:
        try:
            res = callook.get_callsign(call)
            if res.status != EntryStatus.VALID:
                raise CallookError(f"{call.upper()} is {res.status.value.lower()}")
            if args.pretty:
                c.print(
                    Panel.fit(
                        tabulate(asdict(res), True),
                        title=f"Callsign: {call}",
                        border_style=Style(color="green")
                    )
                )
            else:
                print(tabulate(asdict(res)))
        except CallookError as e:
            if args.pretty:
                ec.print(
                    Panel.fit(
                        str(e),
                        title=f"Callsign: {call}",
                        style=Style(color="red"),
                        border_style=Style(color="red")
                    )
                )
            else:
                print(e)
        print()
