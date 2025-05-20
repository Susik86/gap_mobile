import random
from faker import Faker

fake = Faker()

class Users:
    # 🔐 Valid test users for multi-device tests
    VALID_USERS = [

        {"email": "andranik.hayrapetyan@volo.global", "password": "qwe123QWE!@#"}, # User A (iOS)
        {"email": "karlen.aleksanyan@volo.global", "password": "qwe123QWE!@#"}  # User B (Android)

    ]

    # ❌ Fake invalid users for negative testing
    INVALID_USERS = [
        {
            "email": fake.email(),
            "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        },
        {
            "email": fake.email(),
            "password": fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)
        }
    ]

    @staticmethod
    def get_user_a():
        """Returns User A (usually the initiator)"""
        return Users.VALID_USERS[0]

    @staticmethod
    def get_user_b():
        """Returns User B (usually the receiver)"""
        return Users.VALID_USERS[1]

    @staticmethod
    def get_random_valid_user():
        return random.choice(Users.VALID_USERS)

    @staticmethod
    def get_random_invalid_user():
        return random.choice(Users.INVALID_USERS)
