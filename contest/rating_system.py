from django.contrib.auth import get_user_model

from contest.models import Contest


User = get_user_model()


class RatingSystem:
    def __init__(self, contest_id):
        self.contest_id = contest_id
        self.contest = None
        self.users = None
        self.prob = None
        self.seeds = None

    def get_contest(self):
        if self.contest:
            return self.contest
        self.contest = Contest.objects.get(id=self.contest_id)
        return self.contest

    def get_users(self):
        standings = self.get_contest().standings
        users_ids = [ standing.get('id') for standing in standings ]
        self.users = User.objects.filter(id__in=users_ids)
        return self.users

    def generate_probability_matrix(self):
        pass

    def calculate_seeds(self):
        pass
