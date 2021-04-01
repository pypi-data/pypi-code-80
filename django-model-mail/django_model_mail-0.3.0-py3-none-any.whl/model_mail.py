from typing import TYPE_CHECKING, Union, List

from django.core.mail import EmailMessage
from django.forms import ALL_FIELDS

from .library import renderers_library

if TYPE_CHECKING:
    from django.db.models.base import Model


def send_model_mail(
    obj: "Model",
    to: List[str],
    subject: str,
    fields: Union[str, List[str]] = ALL_FIELDS,
    template_name: str = "model_mail/email.html",
):
    body = subject + "\n"
    for field_name in fields:
        field = obj._meta.get_field(field_name)
        value = getattr(obj, field_name)
        body += renderers_library.get_renderer(field).render(value) + "\n"
    message = EmailMessage(
        subject,
        body,
        to=to,
    )
    message.send()
