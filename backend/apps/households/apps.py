from django.apps import AppConfig


class HouseholdsConfig(AppConfig):
    name = "apps.households"

    def ready(self):
        from . import signals  # noqa: F401
