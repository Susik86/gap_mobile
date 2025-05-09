# utils/push_helper.py

import time
import logging
# import requests  # Uncomment if using real API

class PushHelper:
    def __init__(self, platform):
        self.platform = platform
        self.logger = logging.getLogger("mobile_framework_logger")

    def wait_for_push_containing(self, expected_text, timeout=30):
        self.logger.info(f"📬 Waiting for push containing: '{expected_text}'")
        start = time.time()

        while time.time() - start < timeout:
            pushes = self.get_pushes()
            for push in pushes:
                if expected_text.lower() in push.lower():
                    self.logger.info(f"✅ Found push: {push}")
                    return push
            time.sleep(2)

        raise TimeoutError(f"❌ Push containing '{expected_text}' not received within {timeout} seconds.")

    def get_pushes(self):
        # Simulated push list for now
        return [
            # "You are invited to join a team. Tap now to join.",
            "New Genius Pulse launched.Tap now to take the Pulse."
            "Daily check-in reminder"
        ]

        # ✅ Replace the above with a real API call if needed:
        # response = requests.get(f"https://your.push.service/api/pushes?user={self.platform}")
        # return [item["body"] for item in response.json()]
