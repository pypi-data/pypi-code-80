import uuid
from django.contrib.postgres.fields import JSONField
from django.db import models


class FormType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    json = JSONField(blank=True, null=True)
    ui = JSONField(blank=True, null=True)

    title = models.CharField(
        "Form title",
        max_length=250,
        help_text="A title for this form type",
        unique=True,
    )

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
