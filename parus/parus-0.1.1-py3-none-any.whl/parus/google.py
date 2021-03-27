from googleapiclient.discovery import build


def build_google_drive_service(credentials):
    return build('drive', 'v3', credentials=credentials)
