import argparse
import sys

from parus.auth import get_credentials
from parus.search import search_files
from parus.upload import upload_to_drive
from parus.update import update_file


def main(argv):
    p = argparse.ArgumentParser(prog='parus')
    subp = p.add_subparsers(dest='command', required=True)

    search = subp.add_parser('search')
    _credentials_arg(search)
    search.add_argument('-q', '--query')
    search.add_argument('--max-size', type=int, default=50)
    search.add_argument('--paging', action='store_true')
    search.add_argument('-p', '--page-size', type=int, default=20)

    upload = subp.add_parser('upload')
    _credentials_arg(upload)
    upload.add_argument('file')
    upload.add_argument('--name')
    upload.add_argument('--mime')
    upload.add_argument('--folder-id')

    update = subp.add_parser('update')
    _credentials_arg(update)
    update.add_argument('file')
    update.add_argument('--file-id', required=True)

    args = p.parse_args(argv)
    args = vars(args)

    cmd = args.pop('command')
    creds = get_credentials(args.pop('credentials', None))
    args.update(credentials=creds)

    {
        'search': search_files,
        'upload': upload_to_drive,
        'update': update_file,
    }[cmd](**args)

    return 0


def _credentials_arg(p):
    p.add_argument('--credentials', help='Path of credentials json.')


def entry_point():
    sys.exit(main(sys.argv[1:]))
