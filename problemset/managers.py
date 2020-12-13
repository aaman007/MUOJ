from django.db import models
from django.db.models import Case, When


class ProblemManager(models.Manager):

    def filter_preserved_by_ids(self, problem_ids):
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(problem_ids)])
        return self.get_queryset().filter(id__in=problem_ids).order_by(preserved)
