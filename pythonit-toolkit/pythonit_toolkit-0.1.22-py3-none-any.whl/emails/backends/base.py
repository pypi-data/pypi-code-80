from abc import ABC, abstractmethod
from pythonit_toolkit.emails.templates import EmailTemplate



class EmailBackend(ABC):
    @abstractmethod
    def send_email(self, template: EmailTemplate, to: str, subject: str):
        pass
