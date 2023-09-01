import random


class GameManager():
    def __init__(self) -> None:
        self.start_score = 1000
        self.guess_count = 0

    @staticmethod
    def get_random_number():
        return random.randint(1, 100)
