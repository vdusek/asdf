import string
import random


def get_random_string(length: int, with_digits: bool = False) -> str:
    """
    Generate a random string with the desired length.
    """
    chars = string.ascii_lowercase + string.digits if with_digits else string.ascii_lowercase
    random_string = "".join(random.choice(chars) for _ in range(length))
    return random_string
