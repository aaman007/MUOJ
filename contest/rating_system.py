from django.contrib.auth import get_user_model

from contest.models import Contest


User = get_user_model()


class RatingSystem:
    """
    Reference1: https://codeforces.com/blog/entry/102
    Reference2: https://codeforces.com/blog/entry/20762
    """
    def __init__(self, contest_id):
        self.contest_id = contest_id
        self.contest = None
        self.users = None
        self.user_ids = None
        self.prob = None
        self.seeds = None
        self.actual_position = None
        self.rating_changes = None

    def get_contest(self):
        """
        Fetching the contest for which rating system is applied
        """
        if self.contest:
            return self.contest

        self.contest = Contest.objects.get(id=self.contest_id)
        return self.contest

    def get_user_ids(self):
        """
        Fetches all the user_ids of all contestants
        """
        if self.user_ids:
            return self.user_ids

        standings = self.get_contest().standings
        self.user_ids = [standing.get('id') for standing in standings]
        return self.user_ids

    def get_users(self):
        """
        Fetches all users of the contest
        """
        if self.users:
            return self.users

        self.users = User.objects.filter(id__in=self.get_user_ids())
        return self.users

    @staticmethod
    def calculate_probability(ri, rj):
        """
        Formula: Pij = 1 / (1 + 10^((rj-ri) / 400))
        """
        return 1.0 / (1 + 10**((rj-ri)/400.0))

    def get_probability_matrix(self):
        """
        Generating probability matrix for all contestants
        It defines the probability that user A will have a
        better rank than user B with P[A][B]
        """
        if self.prob:
            return self.prob

        self.prob = {}
        for user in self.get_users():
            self.prob[user.id] = {}
            for opponent in self.get_users():
                if user.id == opponent.id:
                    continue
                self.prob[user.id][opponent.id] = self.calculate_probability(
                    user.profile.rating,
                    opponent.profile.rating
                )
        return self.prob

    def get_user_new_seed(self, user_id, rating):
        """
        Calculating seed for a certain user when he has some
        rating X
        """
        if user_id not in self.get_user_ids():
            return {"user": "User didn't participated"}

        seed = 1
        for opponent in self.get_users():
            if user_id == opponent.id:
                continue
            seed += self.calculate_probability(
                opponent.profile.rating,
                rating
            )
        return seed

    def get_user_seed(self, user_id):
        """
        Calculating seed for a certain user
        """
        if user_id not in self.get_user_ids():
            return {"user": "User didn't participated"}

        seed = 1
        for opponent_id in self.get_user_ids():
            if user_id == opponent_id:
                continue
            seed += self.get_probability_matrix()[opponent_id][user_id]
        return seed

    def get_seeds(self):
        """
        Calculating seeds for all contestants
        """
        if self.seeds:
            return self.seeds

        self.seeds = {}
        for user_id in self.get_user_ids():
            self.seeds[user_id] = self.get_user_seed(user_id)
        return self.seeds

    def get_actual_positions(self):
        """
        Getting actual position of all contestants from standings
        """
        if self.actual_position:
            return self.actual_position

        self.actual_position = {}

        position, extra_inc, extra_inc_temp, last_score = 0, 0, 0, -1
        for standing in self.get_contest().standings:
            if standing.get('total_score', 0) != last_score:
                position += 1
                last_score = standing.get('total_score', 0)
                extra_inc += extra_inc_temp
                extra_inc_temp = 0
            else:
                extra_inc_temp += 1

            self.actual_position[standing.get('id', 0)] = position + extra_inc

        return self.actual_position

    def get_user_rating(self, user_id, geo_mean):
        """
        Binary searches for a rating that is close to geo_mean (user seed)
        """
        st, en, best = -5000, 5000, 0

        while st <= en:
            mid = (st+en) // 2
            seed = self.get_user_new_seed(user_id, mid)

            if seed >= geo_mean:
                st = mid+1
                best = mid
            else:
                en = mid-1
        return best

    def get_rating_changes(self):
        if self.rating_changes:
            return self.rating_changes

        """
        Applying the seeds and geometric mean to get all user's
        rating changes
        """
        self.rating_changes = {}
        total = 0
        for user in self.get_users():
            actual_pos = self.get_actual_positions()[user.id]
            predicted_pos = self.get_seeds()[user.id]
            geo_mean = (actual_pos*predicted_pos)**0.5
            new_rating = self.get_user_rating(user.id, geo_mean)
            self.rating_changes[user.id] = (new_rating - user.profile.rating) // 2
            total += self.rating_changes[user.id]

        """
        Setting total participants and number of top participants based on rating
        before contest
        top_contestants = min(total, quadratic_root(total))
        """
        total_participants = len(self.get_user_ids())
        s = min(total_participants, int(total_participants**(1/4.0)))

        """
        Fetching all top participants
        """
        user_ratings = []
        for user in self.get_users():
            user_ratings.append({'id': user.id, 'rating': user.profile.rating})
        top_users = sorted(user_ratings, key=lambda k: -k['rating'])[:s]

        """
        Applying rating change inflation to all contestants
        This make sum of all rating_changes[i] closer to 0
        """
        inc = (-total // total_participants) - 1
        for user_id in self.get_user_ids():
            self.rating_changes[user_id] += inc

        """
        Applying rating change inflation to top contestants
        This stops "Rick getting richer"
        """
        sum_s = 0
        for user in top_users:
            sum_s += self.rating_changes[user.get('id', 0)]
        inc = min(max(-sum_s//s, -10), 0)
        for user in top_users:
            self.rating_changes[user.get('id', 0)] += inc

        return self.rating_changes
