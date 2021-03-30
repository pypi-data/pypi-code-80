"""CLI interface argument parser"""


# Standard library import
import argparse

# Local import
from crontip.__version__ import __version__

parser = argparse.ArgumentParser(
    prog='crontip',
    description="""
    Install crontab from external file.\n
    Backup current crontab to somewhere.
    Edit the backup.
    """,
    epilog="""
        Backup the current crontab before install new one.
    """
)

# Backup
parser.add_argument(
    '-b', '--backup',
    action='store_true',
    help="""
        Backup current crontab into backup folder,
        which located in the default path of installed package.
    """
)

# Edit
parser.add_argument(
    '-e', '--edit',
    action='store_true',
    help="""
        Edit the copy of latest backup of current crontab.
    """
)

# Install
parser.add_argument(
    '-i', '--install',
    action='store_true',
    help="""
        Install the latest ready file by default,
        Appoint a target file is also support.
    """
)

# Appoint file
parser.add_argument(
    '-f', '--file',
    action='store',
    type=str,
    help="""
        Appoint the file which will be installed.
    """
)

# Destination
parser.add_argument(
    '-o', '--output',
    action='store',
    type=str,
    help="""
        Appoint the destination, where store the backup.
    """
)

# Version
parser.add_argument(
    '-v', '--version',
    action='version',
    version='%(prog)s '+__version__
)
