from django.apps import AppConfig


class LibappConfig(AppConfig):
    name = 'libapp'

    def ready(self):
        import libapp.signals