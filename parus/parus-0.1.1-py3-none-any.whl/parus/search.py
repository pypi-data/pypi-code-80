from parus.google import build_google_drive_service

FIELDS = 'files(id, name, mimeType, trashed), nextPageToken'


def search_files(credentials, query=None, max_size=50, paging=False, page_size=20):
    '''See for query: https://developers.google.com/drive/api/v3/search-files
    '''
    drive_service = build_google_drive_service(credentials)
    with drive_service.files() as drive_files:
        token = None
        ps = max_size if not paging else page_size
        cont = True
        while cont:
            res = drive_files.list(q=query, pageSize=ps, pageToken=token, fields=FIELDS).execute()
            files = res.get('files', [])
            for f in files:
                print(f"{f['name']} ({f.get('mimeType', 'unknown')}{', trashed' if f['trashed'] else ''}): {f['id']}")
            token = res.get('nextPageToken', None)
            cont = token is not None
            while cont:
                k = input('<ENTER>: search more results / q: quit > ').lower()
                if k.startswith('q'):
                    cont = False
                elif k != '':
                    continue
                break
