import pathlib

from googleapiclient.http import MediaFileUpload
from parus.config import get_default_folder_id
from parus.google import build_google_drive_service


def upload_to_drive(file, credentials, name=None, mime=None, folder_id=None):
    p = pathlib.Path(file)
    folder = folder_id or get_default_folder_id()

    meta = {'name': name or p.name}
    if folder is not None:
        meta.update(parents=[folder])

    drive_service = build_google_drive_service(credentials)
    with drive_service.files() as drive_files:
        media = MediaFileUpload(p, mimetype=mime, resumable=True)
        uploaded = drive_files.create(body=meta, media_body=media, fields='id, name').execute()
        print('Upload completed: %s (id: %s)' % (uploaded.get('name'), uploaded.get('id')))
