import pathlib

from parus.update import update_file

MODULE = 'parus.update'


class TestUpdateFile:
    def test_update(self, google_drive_api):
        f = pathlib.Path('file/to/update.txt')
        f_id = 'file-id'
        c = google_drive_api.dummy_credentials()
        drive_service, build_drive_service = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        req = google_drive_api.mock_drive_files_update(drive_files)
        mfu, mfu_init = google_drive_api.mock_media_file_upload(MODULE)

        update_file(f, f_id, c)

        build_drive_service.assert_called_once_with(c)
        drive_service.files.assert_called_once()
        mfu_init.assert_called_once_with(f, resumable=True)
        drive_files.update.assert_called_once_with(fileId=f_id, media_body=mfu, fields='id, name')
        req.execute.assert_called_once()
