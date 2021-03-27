import json
import boto3

from typing import Optional
from .base import EmailBackend
from pythonit_toolkit.emails.templates import EmailTemplate


class SESEmailBackend(EmailBackend):
    def __init__(self) -> None:
        super().__init__()
        self.ses = boto3.client('ses')

    def send_email(self, template: EmailTemplate, to: str, subject: str, variables: Optional[dict[str, str]] = None):
        self.ses.send_templated_email(
            Source='noreply@pycon.it',
            Destination={
                'ToAddresses': [
                    to
                ]
            },
            Template=f'pythonit-pastaporto-{template}',
            TemplateData=json.dumps(variables if variables else {})
        )
