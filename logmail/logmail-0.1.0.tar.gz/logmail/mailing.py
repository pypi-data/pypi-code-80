import contextlib
import sys
import os
from traceback import format_exception
from typing import Union, List, Tuple

import emails
from loguru import logger


class Mailer(object):
    def init(
            self,
            smtp_host=None,
            smtp_port=None,
            smtp_timeout=None,
            service_name="MAILER",
            recipient_list=None,
            mail_from=None,
            testing=False,
            test_service_name=None,
            test_recipient_list=None,
            test_mail_from=None,
            traceback_limit=5,
            convert_all_data_to_html=False,
            debug=False
    ):
        self.set_mail_config(
            smtp_timeout=smtp_timeout,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            service_name=service_name,
            recipient_list=recipient_list,
            mail_from=mail_from,
            testing=testing,
            test_service_name=test_service_name,
            test_recipient_list=test_recipient_list,
            test_mail_from=test_mail_from,
            traceback_limit=traceback_limit,
            convert_all_data_to_html=convert_all_data_to_html,
            debug=debug
        )

    def error(self, summary=None, message=None):
        self._logmail("error", "red", summary, message)

    def success(self, summary=None, message=None):
        self._logmail("success", "green", summary, message)

    def debug(self, summary=None, message=None):
        self._logmail("debug", "blue", summary, message)

    def info(self, summary=None, message=None):
        self._logmail("info", "black", summary, message)

    def warning(self, summary=None, message=None):
        self._logmail("warning", "orange", summary, message)

    def critical(self, summary=None, message=None):
        self._logmail("CRITICAL", "red", summary, message)

    def _logmail(self, level: str, color: str, summary: str, message: str):
        if not summary:
            summary = self.SUMMARY.format(level="error", SERVICE_NAME=self.SERVICE_NAME)
        if not message:
            message = self.MESSAGE

        if self.CONVERT_ALL_DATA_TO_HTML:
            summary = self.convert_str_to_html(summary)
            message = self.convert_str_to_html(message)

        result_html_message = """
        <p><strong style="color: {color};">{summary}</strong></p>
        <p>{message}</p>""".format(color=color, summary=summary, message=message)

        service_name = self.SERVICE_NAME
        recipient_list = self.RECIPIENT_LIST
        mail_from = self.MAIL_FROM
        if self.TESTING:
            service_name = self.TEST_SERVICE_NAME
            recipient_list = self.TEST_RECIPIENT_LIST
            mail_from = self.TEST_MAIL_FROM

        subject = "[{service_name} {level}]".format(
            service_name=service_name.upper(), level=level.upper()
        )

        tb = format_exception(*sys.exc_info(), limit=self.TRACEBACK_LIMIT)
        for i, t in enumerate(tb):
            if t == "NoneType: None\n":
                continue
            if i != 0 and i != len(tb) - 1:
                try:
                    tb_text = "<p>{file} <strong style='color: {color};'>{func}</strong></p>".format(
                        file=t.split('", ')[0], func=t.split('", ')[1], color=color
                    )
                except IndexError:
                    tb_text = "<p><strong style='color: {color};'>{tb}</strong></p>".format(
                        color=color, tb=t
                    )
                result_html_message += tb_text
            else:
                result_html_message += "<p><strong style='color: {color};'>{tb}</strong></p>".format(
                    tb=t, color=color
                )

        message = emails.Message(html=result_html_message, subject=subject, mail_from=mail_from)
        message.send(to=recipient_list, smtp=self.SMTP_CONFIG)

    def send_mail(self, subject, message, mail_from, recipient_list):
        message = emails.Message(html=message, subject=subject, mail_from=mail_from or self.MAIL_FROM)
        message.send(to=recipient_list or self.RECIPIENT_LIST, smtp=self.SMTP_CONFIG)

    @staticmethod
    def convert_str_to_html(text: str, separator="\n", tag="p", attrs="", join_base="") -> str:
        """
        Converting one python-string to html content:
        >>> from logmail import convert_str_to_html
        >>> html = convert_str_to_html("Some Text To Be Converted", separator=" ", tag="strong")
            html variable is str which looks like:
                    <strong>Some</strong>
                    <strong>Text</strong>
                    <strong>To</strong>
                    <strong>Be</strong>
                    <strong>Converted</strong>

        :param text: string to convert
        :param separator: character to split
        :param tag: html tag to wrap
        :param attrs: any html tag attributes with values
        :param join_base: base string to join
        :return: html representation of string
        """
        return join_base.join(map(
            lambda t: f"<{tag} {attrs}>" + t + f"</{tag}>",
            text.split(separator)
        ))

    @staticmethod
    def get_persons_emails(persons: List[Union[Tuple[str], str, dict]], index=0, key="email") -> List[str]:
        """
        Parsing mail addresses from list of persons.
        >>> from logmail import get_persons_emails
        >>> persons = [
        >>>     ("Mr. Foo", "foo@example.com"),
        >>>     ("Mr. Bar", "bar@example.com"),
        >>> ]
        >>> emails = get_persons_emails(persons, index=1)
        >>> emails
        >>> ["foo@example.com", "bar@example.com"]

        :param persons: list of persons representation (ex: ADMINS or MANAGERS variable in Django)
        :param index: if "persons" is list of tuples, set index of each element to choose
        :param key: if "persons" is list of dicts, set key of each element to choose
        :return: list of emails like ["foo@example.com", "bar@example.com"]
        """
        if len(persons) <= 0:
            return []
        result_mails = []
        for person in persons:
            if isinstance(person, str):
                result_mails.append(person)  # TODO: add parsing from strings
            elif isinstance(person, tuple):
                result_mails.append(person[index])
            elif isinstance(person, dict) and key in person:
                result_mails.append(person[key])
        return result_mails

    def set_smtp_config(self, host: str, port: int, timeout: int):
        self.SMTP_CONFIG = {
            "host": host,
            "port": port,
            "timeout": timeout,
        }

    def set_mail_config(
            self,
            smtp_host=None,
            smtp_port=None,
            smtp_timeout=None,
            service_name="MAILER",
            recipient_list=None,
            mail_from=None,
            testing=False,
            test_service_name=None,
            test_recipient_list=None,
            test_mail_from=None,
            traceback_limit=5,
            convert_all_data_to_html=False,
            debug=False,
    ):
        self.set_smtp_config(smtp_host, smtp_port, smtp_timeout)
        self.set_debug(debug)
        self.set_traceback_limit(traceback_limit)

        self.MESSAGE = ""
        self.SUMMARY = "{SERVICE_NAME} {level}"

        self.SERVICE_NAME = service_name
        self.RECIPIENT_LIST = recipient_list
        self.MAIL_FROM = mail_from

        self.TESTING = testing

        self.TEST_SERVICE_NAME = test_service_name or service_name
        self.TEST_RECIPIENT_LIST = test_recipient_list or recipient_list
        self.TEST_MAIL_FROM = test_mail_from or mail_from

        self.CONVERT_ALL_DATA_TO_HTML = convert_all_data_to_html

    def set_debug(self, debug):
        self.DEBUG = debug

    def set_traceback_limit(self, traceback_limit):
        self.TRACEBACK_LIMIT = traceback_limit

    @contextlib.contextmanager
    def debugging(self):
        # TODO: add logging for debugging sending process to _logmail method
        self.set_debug(True)
        logger.debug("start sending mail...")
        yield
        logger.debug("mail sent")
        self.set_debug(False)


mailer = Mailer()
