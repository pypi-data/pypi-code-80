import pytest

from unittest.mock import patch

from parus.search import search_files

MODULE = 'parus.search'


class TestSearchFiles:
    def test_search_with_default(self, google_drive_api):
        c = google_drive_api.dummy_credentials()
        drive_service, build_drive_service = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        req = google_drive_api.mock_drive_files_list(drive_files)

        search_files(c)

        build_drive_service.assert_called_once_with(c)
        drive_service.files.assert_called_once()
        drive_files.list.assert_called_once_with(
            q=None, pageSize=50, pageToken=None, fields='files(id, name, mimeType, trashed), nextPageToken')
        req.execute.assert_called_once()

    def test_search_with_query(self, google_drive_api):
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_list(drive_files)

        search_files(c, query='name contains parus')

        drive_files.list.assert_called_once_with(
            **google_drive_api.list_params(q='name contains parus'))

    def test_search_with_max_size(self, google_drive_api):
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_list(drive_files)

        search_files(c, max_size=10)

        drive_files.list.assert_called_once_with(
            **google_drive_api.list_params(pageSize=10))

    def test_search_with_paging_and_default_page_size(self, mocker, google_drive_api):
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_list(drive_files)

        search_files(c, paging=True)

        drive_files.list.assert_called_once_with(
            **google_drive_api.list_params(pageSize=20))

    def test_search_with_paging_and_specified_page_size(self, mocker, google_drive_api):
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_list(drive_files)

        search_files(c, paging=True, page_size=5)

        drive_files.list.assert_called_once_with(
            **google_drive_api.list_params(pageSize=5))

    def test_search_more_and_exit_when_no_additional_result(self, mocker, google_drive_api):
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        req = google_drive_api.mock_drive_files_list(drive_files, results=[
            google_drive_api.drive_files_list_result(token='next-page-token'),
            google_drive_api.drive_files_list_result(token=None),
        ])

        with mock_input(return_values=['']) as input_mock:
            search_files(c, paging=True)

        drive_files.list.assert_has_calls([
            mocker.call(**google_drive_api.list_params(pageToken=None)),
            mocker.call(**google_drive_api.list_params(pageToken='next-page-token')),
        ])
        assert len(req.execute.mock_calls) == 2
        input_mock.assert_called_once()

    def test_ask_more_result_and_quit_intentionally(self, mocker, google_drive_api):
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_list(drive_files, results=[
            google_drive_api.drive_files_list_result(token='next-page-token'),
        ])

        with mock_input(return_values=['q']) as input_mock:
            search_files(c, paging=True)

        drive_files.list.assert_called_once()
        input_mock.assert_called_once()

    def test_ask_repeatedly_when_unexpected_input(self, mocker, google_drive_api):
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_list(drive_files, results=[
            google_drive_api.drive_files_list_result(token='next-page-token'),
        ])

        with mock_input(return_values=['xxx', 'q']) as input_mock:
            search_files(c, paging=True)

        drive_files.list.assert_called_once()
        assert len(input_mock.mock_calls) == 2

    @pytest.mark.parametrize('file_data, expect', [
        ({'id': 'file-id', 'name': 'file-name', 'mimeType': 'mime/type', 'trashed': False},
         'file-name (mime/type): file-id'),
        ({'id': 'file-id', 'name': 'file-name', 'trashed': False},
         'file-name (unknown): file-id'),
        ({'id': 'file-id', 'name': 'file-name', 'mimeType': 'mime/type', 'trashed': True},
         'file-name (mime/type, trashed): file-id'),
    ])
    def test_print_result(self, google_drive_api, file_data, expect):
        c = google_drive_api.dummy_credentials()
        drive_service, _ = google_drive_api.mock_build_google_drive_service(MODULE)
        drive_files = google_drive_api.mock_drive_service_files(drive_service)
        google_drive_api.mock_drive_files_list(drive_files, results=[
            google_drive_api.drive_files_list_result(files=[file_data]),
        ])

        with mock_print() as print_mock:
            search_files(c)

        print_mock.assert_called_once_with(expect)


def mock_input(return_values):
    return patch('builtins.input', side_effect=return_values)


def mock_print():
    return patch('builtins.print')
