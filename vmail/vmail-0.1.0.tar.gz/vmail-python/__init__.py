import base64
import email
from httplib2 import Http
from bs4 import BeautifulSoup
from time import strftime, gmtime
import sys
from apiclient import errors
import requests
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
global SERVICE


class gmailRead:
    def __init__(self, service, user_id='me'):
        self.service = SERVICE
        self.user_id = user_id

    def get_msgids_with_labels(self, label_ids=[]):
        try:
            response = self.service.users().messages().list(
                userId=self.user_id, labelIds=label_ids).execute()

            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']

                response = self.service.users().messages().list(
                    userId=self.user_id, labelIds=label_ids, pageToken=page_token).execute()

                messages.extend(response['messages'])

                #print('... total %d emails on next page [page token: %s], %d listed so far' % (len(response['messages']), page_token, len(messages)))
                # sys.stdout.flush()

            return messages

        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_email(self, msg_id):
        email = {"Body": ""}
        try:
            message = self.service.users().messages().get(
                userId=self.user_id, id=msg_id).execute()  # fetch the message using API
        except:
            raise Exception
        payld = message['payload']  # get payload of the message
        headr = payld['headers']  # get header of the payload

        for info in headr:  # getting the Subject
            if info['name'] == 'Subject':
                msg_subject = info['value']
                email['Subject'] = msg_subject
            else:
                pass
            if info['name'] == 'Date':
                msg_date = info['value']
                email['DateTime'] = msg_date
            else:
                pass
            if info['name'] == 'From':
                msg_from = info['value']
                email['MsgFrom'] = msg_from
            else:
                pass
            if info['name'] == 'content-type':
                msg_encoding = info['value'] or 'UTF-8'
                emailEncoding = msg_encoding

        def bodyHelper(payld, email):
            if payld["mimeType"] == "text/plain":
                if info['name'] == 'content-type':
                    msg_encoding = info['value'] or 'UTF-8'
                    emailEncoding = msg_encoding
                email["Body"] += base64.urlsafe_b64decode(
                    payld["body"]["data"].decode(emailEncoding))
            elif bool(payld["parts"]):
                for part in payld["parts"]:
                    return bodyHelper(part, email)
        bodyHelper(payld, email)
        return email


def start(userID='me', credentialsFile="credentials.json"):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    try:
        if not os.path.exists(credentialsFile):
            raise EZGmailException(
                'Can\'t find credentials file at %s. You can download this file from https://developers.google.com/gmail/api/quickstart/python and clicking "Enable the Gmail API". Rename the downloaded file to credentials.json.'
                % (os.path.abspath(credentialsFile))
            )

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentialsFile, SCOPES)
                creds = flow.run_local_server(port=5000)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        SERVICE = build('gmail', 'v1', credentials=creds)


