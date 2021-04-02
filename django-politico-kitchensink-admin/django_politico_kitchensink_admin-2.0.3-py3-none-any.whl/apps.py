from django.apps import AppConfig


class KitchensinkConfig(AppConfig):
    name = "kitchensink"

    def ready(self):
        from kitchensink import signals  # noqa
