import random


def get_random_code():
    return "%06d" % random.randint(0, 999999)
