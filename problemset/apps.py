from django.apps import AppConfig


class ProblemsetConfig(AppConfig):
    name = 'problemset'

    def ready(self):
        import problemset.signals
