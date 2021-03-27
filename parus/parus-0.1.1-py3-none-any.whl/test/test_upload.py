import pathlib

from parus.upload import upload_to_drive

MODULE = 'parus.upload'


class TestUploadToDrive:
    def test_upload_with_defaults(self, parus_config, google_drive_api):
        get_default_folder_id = parus_config.mock_get_default_folder_id(MODULE, folder_id=None)
        f = pathlib.Path('file/to/upload.txt')
        c = google_drive_api.dummy_credentials()
        drive_service, build_drive_service = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        req = google_drive_api.mock_drive_files_create_and_execute(drive_files)
        mfu, mfu_init = google_drive_api.mock_media_file_upload(MODULE)

        upload_to_drive(f, c)

        get_default_folder_id.assert_called_once()
        build_drive_service.assert_called_once_with(c)
        drive_service.files.assert_called_once()
        mfu_init.assert_called_once_with(f, mimetype=None, resumable=True)
        meta = {
            'name': f.name,
        }
        drive_files.create.assert_called_once_with(body=meta, media_body=mfu, fields='id, name')
        req.execute.assert_called_once()

    def test_upload_to_default_folder(self, mocker, parus_config, google_drive_api):
        parus_config.mock_get_default_folder_id(MODULE, folder_id='default-folder-id')
        f = pathlib.Path('file/to/upload.txt')
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_create_and_execute(drive_files)
        google_drive_api.mock_media_file_upload(MODULE)

        upload_to_drive(f, c)

        meta = {
            'name': f.name,
            'parents': ['default-folder-id'],
        }
        drive_files.create.assert_called_once_with(body=meta, media_body=mocker.ANY, fields=mocker.ANY)

    def test_upload_to_specified_folder(self, mocker, parus_config, google_drive_api):
        get_default_folder_id = parus_config.mock_get_default_folder_id(MODULE)
        f = pathlib.Path('file/to/upload.txt')
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_create_and_execute(drive_files)
        google_drive_api.mock_media_file_upload(MODULE)

        upload_to_drive(f, c, folder_id='my-folder-id')

        get_default_folder_id.assert_not_called()
        meta = {
            'name': f.name,
            'parents': ['my-folder-id'],
        }
        drive_files.create.assert_called_once_with(body=meta, media_body=mocker.ANY, fields=mocker.ANY)

    def test_upload_with_name(self, mocker, parus_config, google_drive_api):
        parus_config.mock_get_default_folder_id(MODULE)
        f = pathlib.Path('file/to/upload.txt')
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_create_and_execute(drive_files)
        google_drive_api.mock_media_file_upload(MODULE)

        upload_to_drive(f, c, name='file-name.txt')

        meta = {
            'name': 'file-name.txt',
        }
        drive_files.create.assert_called_once_with(body=meta, media_body=mocker.ANY, fields=mocker.ANY)

    def test_upload_with_mime(self, mocker, parus_config, google_drive_api):
        parus_config.mock_get_default_folder_id(MODULE)
        f = pathlib.Path('file/to/upload.txt')
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_create_and_execute(drive_files)
        _, mfu_init = google_drive_api.mock_media_file_upload(MODULE)

        upload_to_drive(f, c, mime='text/plain')

        mfu_init.assert_called_once_with(f, mimetype='text/plain', resumable=True)
