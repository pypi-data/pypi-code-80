"""This is the entry point of crontip"""


# Local application imports
from crontip.cli import parser
from crontip.crontab import CronTab
from crontip.file_operate import find_latest_file
from crontip.linux_cmd import run_cmd
from crontip import __path__


# The defualt path of a installed package, there is crontip
PKG_HOME = __path__[0]
BACKUP_FOLDER = f'{PKG_HOME}/backup/'
READY_FOLDER = f'{PKG_HOME}/ready/'


def main():
    args = parser.parse_args()

    # Backup
    if args.backup:
        # Appoint backup destination
        if args.output:
            crontab = CronTab(backup_path=args.output)
        else:
            crontab = CronTab(backup_folder=BACKUP_FOLDER)

        backup_dest = crontab.backup()
        print(f'current crontab backuped in {backup_dest}')

    # Install
    if args.install:
        print(
            'Install will overide the current crontab,\n'
            + 'you should backup before install.\n'
            + 'continue?'
        )

        # Check if user input is valid
        try:
            is_valid_decision = False
            while not is_valid_decision:
                decision = input('y/yes or n/no')
                if decision in 'y yes n no'.split():
                    is_valid_decision = True
        # Exit whole program when invalid
        except KeyboardInterrupt:
            raise(SystemExit)

        if 'n' in decision or 'no' in decision:
            raise(SystemExit)
        else:
            # Appoint the file that will be install
            if args.file:
                target = args.file
            else:
                # Target is READY file by default
                latest = find_latest_file(READY_FOLDER)
                target = READY_FOLDER + latest

            # Set the target path for install
            crontab = CronTab(ready_path=target)
            crontab.install()

    # Edit crontab
    if args.edit:
        latest_file_name = find_latest_file(BACKUP_FOLDER)

        src = BACKUP_FOLDER + latest_file_name
        dest = READY_FOLDER + latest_file_name

        # Latest backup will be copied befor editing
        run_cmd(f'cp {src} {dest}')
        run_cmd(f'vim {dest}')


if __name__ == '__main__':
    main()
