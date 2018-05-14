from importlib import import_module

from django.apps import AppConfig as BaseAppConfig

class AppConfig(BaseAppConfig):

    name = "forums"
    label = "forums"
    verbose_name = "Fourms"

    def ready(self):
        import_module("forums.receivers")
