import click
import json
from foundry import Foundry
from foundry.models import FoundrySpecification

from typing import List, Dict, Optional, Any
from pydantic import BaseModel
import pandas as pd

from joblib import Parallel, delayed
import multiprocessing
import pandas as pd

num_cores = multiprocessing.cpu_count()


@click.command("install")
@click.option(
    "--file", default="./foundry.json", help="Use which file to create data environment"
)
@click.option(
    "--globus",
    default=False,
    help="If True, uses Globus to download the files, otherwise https",
)
@click.option("--interval", default=3, help="Polling interval in seconds. Default 3s")
@click.option(
    "--verbose",
    default=False,
    help="If True, show more info about the build process",
)
def install(file, globus, interval, verbose):
    # Call SDK function to load specification

    """Simple program that downloads and caches Foundry datasets from a specification file"""

    def start_download(ds, interval=interval, globus=False):
        print("=== Fetching Data Package {} ===".format(ds.name))
        f = Foundry().load(ds.name, download=False)
        f = f.download(interval=interval, globus=globus)
        return {"success": True}

    with open(file, "r") as fp:
        if verbose:
            print("** Loading specification")
            print(f"** Running {num_cores} parallel transfers")
            print(f"** Monitoring with interval {interval} seconds")
            print("** Removing duplicate datasets")

        fs = FoundrySpecification(**json.load(fp))
        fs.remove_duplicate_dependencies()

        results = Parallel(n_jobs=num_cores)(
            delayed(start_download)(ds, interval=interval, globus=globus)
            for ds in fs.dependencies
        )


if __name__ == "__main__":
    install()
