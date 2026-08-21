import random
import string

mobile_prefix_list = [
    "0900",
    "0901",
    "0902",
    "0903",
    "0904",
    "0905",
    "0906",
    "0907",
    "0908",
    "0909",
    "0940",
    "0941",
    "0942",
    "0943",
    "0944",
    "0945",
    "0946",
    "0947",
    "0948",
    "0949",
    "0950",
    "0951",
    "0957",
    "0959",
    "0962",
    "0964",
    "0965",
    "0966",
    "0967",
    "0969",
    "0973",
    "0974",
    "0975",
    "0976",
    "0977",
    "0978",
    "0979",
    "0980",
    "0981",
    "0983",
    "0984",
    "0985",
    "0990",
    "0991",
    "0992",
    "0993",
    "0994",
    "0995",
    "0996",
    "0997",
    "0998",
    "0999",
]


class RandomHelper:

    @staticmethod
    def random_string(length=8):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def random_number(length=4):
        return random.randint(10 ** (length - 1), 10**length - 1)

    @staticmethod
    def generate_phone_mobile():
        prefix = random.choice(mobile_prefix_list)
        postfix = str(random.randrange(111111, 999999, 6))
        number = prefix + postfix
        return number
