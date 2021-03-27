import pathlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from parus.config import get_default_credentials_file, token_file_for


SCOPES = [
    # https://developers.google.com/identity/protocols/oauth2/scopes#drive
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]
_FLOW_SERVER_PORT = 0


def get_credentials(credentials_file=None):
    creds_file = credentials_file and pathlib.Path(credentials_file) or get_default_credentials_file()
    if not creds_file.exists():
        raise RuntimeError('Credentials file not found.'
                           ' Specify by --credentials option,'
                           ' or put credentials.json in $HOME/.parus/')

    token_file = token_file_for(creds_file)
    creds = _try_load_credentials(token_file)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
        creds = flow.run_local_server(port=_FLOW_SERVER_PORT)
    with open(pathlib.Path(token_file), 'w') as fp:
        fp.write(creds.to_json())
    return creds


def _try_load_credentials(token_file):
    if token_file.exists():
        return Credentials.from_authorized_user_file(token_file, SCOPES)
    return None
