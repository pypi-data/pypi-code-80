import argparse
from digital_hydrant.__version__ import version

parser = argparse.ArgumentParser(
    description="Run Digital-Hydrant data collections",
    epilog="By default, both collection and upload will execute unless otherwise specified",
)
parser.add_argument(
    "-c",
    "--collect",
    action="store_true",
    help="dictates that data collection should be run",
)
parser.add_argument(
    "-u",
    "--upload",
    action="store_true",
    help="dictates that stored data should be uploaded",
)
parser.add_argument(
    "-cq",
    "--clear-queue",
    action="store_true",
    help="delete all entries from local database",
)
parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version}")


args = parser.parse_args()
