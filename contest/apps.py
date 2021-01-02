from django.apps import AppConfig


class ContestConfig(AppConfig):
    name = 'contest'

    def ready(self):
        import contest.signals