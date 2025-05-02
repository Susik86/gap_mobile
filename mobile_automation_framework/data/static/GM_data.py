import random
import string

from faker import Faker

fake = Faker()

class GM_data:

    @staticmethod
    def _strong_random_string(length=12):
        while True:
            chars = (
                    random.choice(string.ascii_lowercase) +
                    random.choice(string.ascii_uppercase) +
                    random.choice(string.digits) +
                    random.choice("!@#$%^&*()-_=+[]{}")
            )
            chars += ''.join(random.choices(
                string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}",
                k=length - 4
            ))
            result = ''.join(random.sample(chars, len(chars)))

            if (any(c.islower() for c in result) and
                    any(c.isupper() for c in result) and
                    any(c.isdigit() for c in result) and
                    any(c in "!@#$%^&*()-_=+[]{}" for c in result)):
                return result

    @staticmethod
    def get_random_create_GM_screen_data():
        return {
            "team_name_field": GM_data._strong_random_string(),
            "project_name_field": GM_data._strong_random_string(),
            "outcome_field": GM_data._strong_random_string(),
        }