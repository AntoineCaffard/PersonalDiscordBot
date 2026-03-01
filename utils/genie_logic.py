import json
import random

FILE_PATH = "data/divination.json"

class GenieLogic:

    @staticmethod
    def get_random_answer() :

        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return random.choice(data["phrases"])