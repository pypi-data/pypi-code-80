import argparse
from pathlib import Path


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='arkive')

    commands = parser.add_subparsers(dest='cmd')

    show = commands.add_parser('show', help='display music collection inside a given folder.')
    show.add_argument('folder', type=Path)

    flat = commands.add_parser('flat', help='flatten music files inside a given folder.')
    flat.add_argument('folder', type=Path)
    flat.add_argument('-o', '--output', type=Path)

    nest = commands.add_parser('nest', help='nesting music files inside a given folder.')
    nest.add_argument('folder', type=Path)
    nest.add_argument('-o', '--output', type=Path)

    return parser.parse_args()


def music_show(folder: Path):
    assert folder.exists() and folder.is_dir(), f'\'{folder}\' is not a directory.'

    from arkive.music.show import show_music_collection
    from arkive.utility.table import make_table

    header, content = show_music_collection(folder)
    table = make_table(header, content)
    print(table)


def music_flat(folder: Path, output: Path = None):
    assert folder.exists() and folder.is_dir(), f'\'{folder}\' is not a directory.'
    if output:
        assert output.is_dir()
    else:
        output = folder

    from arkive.music.flat import flat_music_collection
    flat_music_collection(folder, output)


def music_nest(folder: Path, output: Path = None):
    assert folder.exists() and folder.is_dir(), f'\'{folder}\' is not a directory.'
    if output:
        assert output.is_dir()
    else:
        output = folder

    from arkive.music.nest import nest_music_collection
    nest_music_collection(folder, output)


def main():
    args = cli()
    if args.cmd == 'show':
        music_show(args.folder)
    elif args.cmd == 'flat':
        music_flat(args.folder, args.output)
    elif args.cmd == 'nest':
        music_nest(args.folder, args.output)


if __name__ == '__main__':
    main()
