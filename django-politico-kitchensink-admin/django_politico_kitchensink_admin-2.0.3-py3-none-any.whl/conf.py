"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""

from django.conf import settings as project_settings


class Settings:
    pass


Settings.AUTH_DECORATOR = getattr(
    project_settings,
    "KITCHENSINK_AUTH_DECORATOR",
    "django.contrib.admin.views.decorators.staff_member_required",
)

Settings.SECRET_KEY = getattr(
    project_settings, "KITCHENSINK_SECRET_KEY", "a-bad-secret-key"
)

Settings.API_ENDPOINT = getattr(
    project_settings,
    "KITCHENSINK_API_ENDPOINT",
    "https://kitchensink.politicoapps.com/",
)

Settings.PUBLISH_DOMAIN = getattr(
    project_settings, "KITCHENSINK_PUBLISH_DOMAIN", "https://www.politico.com"
)

Settings.PREVIEW_DOMAIN = getattr(
    project_settings,
    "KITCHENSINK_PUBLISH_DOMAIN",
    "http://staging.interactives.politico.com.s3.amazonaws.com",
)

Settings.PUBLISH_PATH = getattr(
    project_settings,
    "KITCHENSINK_PUBLISH_PATH",
    "/interactives/apps/kitchensink",
)

Settings.GOOTENBERG_TOKEN = getattr(
    project_settings,
    "KITCHENSINK_GOOTENBERG_TOKEN",
    None,
)

Settings.GOOTENBERG_ENDPOINT = getattr(
    project_settings,
    "KITCHENSINK_GOOTENBERG_ENDPOINT",
    None,
)

Settings.GOOTENBERG_DEFAULT_DIRECTORY = getattr(
    project_settings,
    "KITCHENSINK_GOOTENBERG_DEFAULT_DIRECTORY",
    None,
)

Settings.AWS_ACCESS_KEY_ID = getattr(
    project_settings, "KITCHENSINK_AWS_ACCESS_KEY_ID", None
)

Settings.AWS_SECRET_ACCESS_KEY = getattr(
    project_settings, "KITCHENSINK_AWS_SECRET_ACCESS_KEY", None
)

Settings.AWS_REGION = getattr(
    project_settings, "KITCHENSINK_AWS_REGION", None
)

Settings.AWS_S3_PRODUCTION_BUCKET = getattr(
    project_settings, "KITCHENSINK_AWS_S3_PRODUCTION_BUCKET", None
)

Settings.AWS_S3_PREVIEW_BUCKET = getattr(
    project_settings, "KITCHENSINK_AWS_S3_PREVIEW_BUCKET", None
)

settings = Settings
