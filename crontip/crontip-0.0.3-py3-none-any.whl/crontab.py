"""Interact with crontab"""


# Standard library import
from datetime import datetime

# Local application imports
from crontip.linux_cmd import get_output, get_result
from crontip.file_operate import find_latest_file, write_file, read_file


class CronTab:
    def __init__(
        self, user: str = None,
        backup_folder: str = None, backup_path: str = None,
        crontab: str = None,
        ready_folder: str = None, ready_path: str = None
    ) -> None:
        self.user = user
        self.backup_folder = backup_folder
        self.backup_path = backup_path
        self.crontab = crontab
        self.ready_folder = ready_folder
        self.ready_path = ready_path

    def __repr__(self) -> str:
        return vars(self)

    def read(self) -> None:
        """
        Read the current installed crontab,
        set it into self.crontab.
        """
        self.crontab = get_output('crontab -l').split('\n')

    def backup(self):
        """Backup user's crontab file into `backup_folder`."""

        self.read()

        # An external crontab file without empty line at the end of it
        # cannot be installed successfully
        if self.crontab[-1] != '\n':
            self.crontab.append('\n')

        # Appoint the destination
        if self.backup_path is not None:
            write_file(self.crontab, dest=self.backup_path)
            dest = self.backup_path
        else:
            timestamp = '-'.join(str(datetime.now()).split())
            folder = self.backup_folder
            extension = '.bk'
            name = timestamp + extension
            # Store the backup into BACKUP_FOLDER by default
            write_file(
                self.crontab,
                save_folder=folder,
                file_name=name
            )

            # Let user know where the current backup stored
            dest = folder + name

        return dest

    def load(self, file=None, path=None):
        """
        Load crontab file in `self.crontab`.
        Load backup by default.
        """
        if path:
            self.crontab_path = path
            self.crontab = read_file(path)
        else:
            if file is None:
                latest = find_latest_file(self.backup_path)
                self.crontab = read_file(self.backup_path + latest)
            else:
                self.crontab = file

    def install(self):
        """
        Install crontab.
        """
        result = get_result('crontab {}'.format(self.ready_path))

        if result.stderr:
            print(result.stderr)
        else:
            print('install succesfully!')
