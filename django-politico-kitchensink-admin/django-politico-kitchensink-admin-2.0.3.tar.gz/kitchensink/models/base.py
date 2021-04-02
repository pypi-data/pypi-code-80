import uuid
from django.contrib.postgres.fields import JSONField
from django.db import models
from kitchensink.conf import settings as app_settings
from kitchensink.utils.gootenberg import gootenberg


class BasePublished:
    def production_url(self):
        return "{}{}{}".format(
            app_settings.PUBLISH_DOMAIN,
            app_settings.PUBLISH_PATH,
            self.sink_publish_path(),
        )

    def preview_url(self):
        return "{}{}{}".format(
            app_settings.PREVIEW_DOMAIN,
            app_settings.PUBLISH_PATH,
            self.sink_publish_path(),
        )


class BaseSink(models.Model, BasePublished):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    google_id = models.SlugField("Google Doc ID", help_text="Doc ID from URL")
    validation_schema = JSONField(
        blank=True, null=True, help_text="JSON Schema"
    )

    VERSION_CHOICES = [("v2", "v2")]

    version = models.CharField(
        max_length=2,
        choices=VERSION_CHOICES,
        blank=False,
        null=False,
        default="v2",
        help_text="Should be the latest version when created.",
    )

    last_updated = models.DateTimeField(auto_now=True)
    last_published = models.DateTimeField(blank=True, null=True)

    def short_id(self):
        return self.google_id[0:12]

    def sink_publish_path(self):
        return "/{}/data.json".format(self.short_id())

    def get_last_content_modified(self):
        resp = gootenberg(
            '/drive/getLastModified/',
            {"id": self.google_id}
        )
        return resp.text

    class Meta:
        abstract = True
