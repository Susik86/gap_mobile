import random
from faker import Faker

fake = Faker()

class Users:
    VALID_USERS = [
        # {"email": "susanna.karapetyan@volo.global", "password": "qwe123QWE!@#"},
        # {"email": "anahit.arustamyan@volo.global", "password": "qwe123QWE!@#"},
        {"email": "NewLGOBCO1@mailinator.com", "password": "qwe123QWE!@#"}
    ]


    # Generate fake invalid users dynamically
    INVALID_USERS = [
        {"email": fake.email(), "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)},
        {"email": fake.email(), "password": fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)}
    ]

    @staticmethod
    def get_random_valid_user():
        return random.choice(Users.VALID_USERS)

    @staticmethod
    def get_random_invalid_user():
        return random.choice(Users.INVALID_USERS)
