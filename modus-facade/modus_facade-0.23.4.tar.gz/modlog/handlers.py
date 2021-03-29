"""Provide a custom handler for ModLog."""

from datetime import datetime
from datetime import timedelta
import logging
import os

from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


class CloudLoggingHandler(logging.Handler):
    """Log message to Google Cloud Logging endpoint.

    Instead of shipping logs to Google's Cloud Logging system using something
     like a log aggregation agent, this handler allows you to stream logs
     message by message the logging endpoint.
    If the logging endpoint becomes unavailable, the handler will fail over to
     sending an alert via email using the Sendgrid email SaaS API.

    It is worth noting that this version does NOT work asynchronously. The
     handler will wait for a response from the Cloud logging API and this will
     be a blocking aaction in your application wherever log messages are
     emitted. Future versions will update this capability but for now, be
     aware.
    """

    def __init__(self, project_id, sendgrid_api=None, failover_email=None,
                 fail_from_address=None, fail_notify_interval=60,
                 sendgrid_fallback=False):
        """Configure Cloud Logging handler instance.

        :param project_id: Google Cloud Project ID
        :param sendgrid_api: Anedgrid API key for fallback email
        :param failover_email: email address of recipient of
            fallback logging email
        :param fail_from_address: email address of sender of
            fallback logging email
        :param fail_notify_interval: interval between notification
            emails if failure of handler persists
        :param sendgrid_fallback: should we fallback to sendgrid incase of
            handler failure
        """
        logging.Handler.__init__(self)
        self.project_id = project_id
        self.sendgrid_fallback = sendgrid_fallback

        self.sendgrid_api = sendgrid_api
        self.failover_email = failover_email
        self.fail_from_address = fail_from_address
        self.fail_notify_interval = fail_notify_interval

        credentials = GoogleCredentials.get_application_default()
        self.logging_api = build('logging', 'v2beta1', credentials=credentials)
        self.track_exceptions = {}

    def emit(self, record):
        """Format log record to be sent to Cloud Logging API.

        :param record: logging record
        """
        log_name = "projects/{}/logs/{}".format(self.project_id, record.name)

        req = self.logging_api.entries().write(
                body={
                    "entries": [
                        {
                            "severity": record.levelname,
                            "jsonPayload": {
                                "module": record.module,
                                "message": record.getMessage(),
                                "lineno": record.lineno,
                                "pathname": record.pathname,
                                "filename": record.filename,
                                "processName": record.processName,
                                "threadName": record.threadName,
                            },
                            "logName": log_name,
                            "resource": {
                                "type": "global",
                            }
                        }
                    ]
                }
        )

        # If the API is dead, for whatever reason, try send an email every
        # now and then
        try:
            req.execute()
        except Exception as e:
            if self.sendgrid_fallback:
                pass


class MockLoggingHandler(logging.Handler):
    """Mock a logging handler to hold the messages to check in testing.

    Messages are available from an instance's ``messages`` dict, in order,
    indexed by a lowercase log level string (e.g., 'debug', 'info', etc.).
    """

    def __init__(self, *args, **kwargs):
        """Instantiate the Mock Logger with common log levels."""
        self.messages = {'debug': [], 'info': [], 'warning': [], 'error': [],
                         'critical': []}
        super(MockLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        """Store a message from ``record`` in the instance's ``messages`` dict.

        :param record: logging record to be emitted to the dict
        :type record:  logging.LogRecord
        :return: None
        :rtype: None
        """
        self.acquire()
        try:
            self.messages[record.levelname.lower()].append(record.getMessage())
        finally:
            self.release()

    def reset(self):
        """Delete the stored list of messages.

        :return: None
        :rtype: None
        """
        self.acquire()
        try:
            for message_list in self.messages.values():
                del message_list[:]
        finally:
            self.release()
