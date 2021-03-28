import json
import os
import random


json_file = os.path.join(os.path.dirname(__file__), 'answers.json')
answers = []

with open(json_file) as r:
    answers.extend(json.load(r)['answers'])


def get_answer() -> str:
    """
    Gets an answer from Van's Eight Ball

    :return: the answer
    """
    return answers[random.randrange(0, len(answers))]


if __name__ == '__main__':
    print(get_answer())
