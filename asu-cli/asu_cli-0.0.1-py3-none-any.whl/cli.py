import sys
from typing import List

import typer

import asu.display as display
import asu.s3 as s3

app = typer.Typer(help="AWS S3 CLI utils")


@app.command()
def sse() -> None:
    """List default encryption for all buckets"""
    display.pretty_print(s3.describe_all_buckets_encryption())


@app.command()
def tags(key: str) -> None:
    """List tag for all buckets"""
    display.pretty_print(s3.describe_all_buckets_tags(key))


def main(args: List[str] = sys.argv[1:]) -> None:
    app(args)


if __name__ == "__main__":
    main()
