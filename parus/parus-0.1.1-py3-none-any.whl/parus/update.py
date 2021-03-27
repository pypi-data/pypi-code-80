import pathlib

from googleapiclient.http import MediaFileUpload
from parus.google import build_google_drive_service


def update_file(file, file_id, credentials):
    p = pathlib.Path(file)

    drive_service = build_google_drive_service(credentials)
    with drive_service.files() as drive_files:
        media = MediaFileUpload(p, resumable=True)
        updated = drive_files.update(fileId=file_id, media_body=media, fields='id, name').execute()
        print('Update completed: %s (%s)' % (updated.get('name'), updated.get('id')))
