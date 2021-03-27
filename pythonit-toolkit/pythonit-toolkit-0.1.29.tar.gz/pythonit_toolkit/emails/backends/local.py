from typing import Optional
from .base import EmailBackend
from pythonit_toolkit.emails.templates import EmailTemplate


class LocalEmailBackend(EmailBackend):
    def send_email(self, template: EmailTemplate, to: str, subject: str, variables: Optional[dict[str, str]] = None):
        print(f"=== Email sending ===")
        print(f"Template: {template}")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Variables: {str(variables)}")
        print(f"=== End Email sending ===")
