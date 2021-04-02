from .mailing import mailer

convert_str_to_html = mailer.convert_str_to_html
get_persons_emails = mailer.get_persons_emails

__all__ = ["mailer", "convert_str_to_html", "get_persons_emails"]

__version__ = "0.1.0"
__author__ = "danila_charushin"

