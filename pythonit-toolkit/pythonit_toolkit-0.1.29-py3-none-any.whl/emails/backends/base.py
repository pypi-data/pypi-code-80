from abc import ABC, abstractmethod
from typing import Optional
from pythonit_toolkit.emails.templates import EmailTemplate



class EmailBackend(ABC):
    @abstractmethod
    def send_email(self, template: EmailTemplate, to: str, subject: str, variables: Optional[dict[str, str]] = None):
        pass
