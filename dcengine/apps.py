from django.apps import AppConfig
from django.conf import settings
import importlib


class EngineConfig(AppConfig):
    name = 'dcengine'

    def ready(self):
        """Engines modules must be imported for EngineClasses self registration"""
        for app in settings.INSTALLED_APPS:
            try:
                module = importlib.import_module(app)
                importlib.import_module(module.__name__ + '.' + 'dcengine')
            except ImportError:
                pass
