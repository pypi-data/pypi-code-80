import uuid
from .base import BasePublished
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField


class FormContent(models.Model, BasePublished):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(
        "Content title",
        max_length=250,
        help_text="A title for this form content",
    )

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    data = JSONField(blank=True, null=True)

    VERSION_CHOICES = [("v2", "v2")]

    version = models.CharField(
        max_length=2,
        choices=VERSION_CHOICES,
        blank=False,
        null=False,
        default="v2",
        help_text="Should be the latest version when created.",
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="forms",
    )

    type = models.ForeignKey(
        "FormType",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="contents",
        related_query_name="contents",
    )

    last_updated = models.DateTimeField(auto_now=True)
    last_published = models.DateTimeField(blank=True, null=True)

    def sink_publish_path(self):
        return "/forms/{}/data.json".format(self.short_id())

    def short_id(self):
        return self.id.hex[0:12]

    def get_data(self):
        return {
            "meta": {
                "source": "kitchensink",
                "version": self.version,
                "lastModified": (
                    self.last_updated.isoformat()
                    if self.last_updated
                    else None
                ),
                "lastPublished": (
                    self.last_published.isoformat()
                    if self.last_published
                    else None
                ),
                "type": self.type.title,
                "project": (
                    self.project.title
                    if self.project
                    else None
                )
            },
            "content": self.data
        }

    def __str__(self):
        return self.title
