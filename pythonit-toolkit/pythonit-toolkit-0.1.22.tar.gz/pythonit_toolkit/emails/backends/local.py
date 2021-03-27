import logging
from .base import EmailBackend
from pythonit_toolkit.emails.templates import EmailTemplate


logger = logging.getLogger(__file__)

class LocalEmailBackend(EmailBackend):
    def send_email(self, template: EmailTemplate, to: str, subject: str):
        logger.debug(f"=== Email sending ===")
        logger.debug(f"Template: {template}")
        logger.debug(f"To: {to}")
        logger.debug(f"Subject: {subject}")
