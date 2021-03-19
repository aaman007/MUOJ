from django.db import models
from django.db.models import Case, When, Count, Q


class ProblemManager(models.Manager):

    def filter_preserved_by_ids(self, problem_ids):
        """
        Filters problems by preserving their id order
        """
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(problem_ids)])
        return self.filter(id__in=problem_ids).order_by(preserved)

    def filter_preserved_by_ids_with_count(self, problem_ids, contest_id=None, current_user=None):
        """
        Filters problems by preserving their id order ( using dictionary)
        and solve_count for each problem under a contest
        Returns a list of problem instances
        """
        qs = self.filter(id__in=problem_ids).annotate(
            solve_count=Count(
                'submissions__user',
                filter=Q(submissions__status='AC', submissions__contest=contest_id),
                distinct=True
            ),
            is_solved=Count(
                'submissions__user',
                filter=Q(
                    submissions__status='AC',
                    submissions__contest=contest_id
                ),
                submissions__user=current_user
            )
        )
        dt = {problem.id: problem for problem in qs}
        return [dt[p_id] for p_id in problem_ids]
