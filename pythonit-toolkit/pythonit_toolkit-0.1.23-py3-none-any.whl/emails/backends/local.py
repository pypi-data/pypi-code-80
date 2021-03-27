import logging
from .base import EmailBackend
from pythonit_toolkit.emails.templates import EmailTemplate


logger = logging.getLogger(__file__)

class LocalEmailBackend(EmailBackend):
    def send_email(self, template: EmailTemplate, to: str, subject: str):
        logger.info(f"=== Email sending ===")
        logger.info(f"Template: {template}")
        logger.info(f"To: {to}")
        logger.info(f"Subject: {subject}")
