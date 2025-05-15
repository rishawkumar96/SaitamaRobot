# SibylSystem.py

class GeneralException(Exception):
    def __init__(self, message="A system error occurred."):
        super().__init__(message)
        self.message = message


class PsychoPass:
    def __init__(self):
        self.user_scores = {}

    def scan_user(self, user_id, behavior_score):
        # Simulate analysis logic
        if user_id not in self.user_scores:
            self.user_scores[user_id] = 0
        self.user_scores[user_id] += behavior_score
        return self.user_scores[user_id]

    def is_dangerous(self, user_id):
        return self.user_scores.get(user_id, 0) > 100

    def get_crime_coefficient(self, user_id):
        return self.user_scores.get(user_id, 0)
