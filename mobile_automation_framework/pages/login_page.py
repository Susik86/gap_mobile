import logging

from data.static.strings.en import StringsEn
from .base_page import BasePage
from data.locators.login_locators import LoginLocators
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    def __init__(self, driver, platform):
        super().__init__(driver)
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger
        self.logger.info(f"🔍 Initializing LoginPage with platform: {platform}")
        self.platform = platform  # ✅ Store platform
        self.locators = LoginLocators.get_locators("LOGIN_PAGE", platform)  # ✅ Ensure platform is passed

        if not self.locators:
            self.logger.error(f"❌ No locators found for platform: {platform}")
            raise ValueError(f"❌ No locators found for platform: {platform}")

    def open_app(self):
        """Ensure the app opens to the login screen before tests."""
        try:
            self.logger.info(f"🔄 Verifying that the login screen is displayed on {self.platform}...")
            login_button_locator = self.locators.get("login_button")

            if not login_button_locator:
                self.logger.error(f"❌ 'login_button' locator not found for {self.platform}")
                raise KeyError(f"❌ 'login_button' locator not found for {self.platform}")

            self.wait_for_element(login_button_locator)
            self.logger.info(f"✅ Login screen is displayed on {self.platform}.")
        except Exception as e:
            self.logger.error(f"❌ Error while opening app on {self.platform}: {e}", exc_info=True)
            raise

    def login(self, email, password, expect_failure=False):
        """Perform login with email and password."""
        login_type = "invalid" if expect_failure else "valid"
        self.logger.info(f"🔹 Performing {login_type} login on {self.platform} with email: {email}")

        try:
            email_field_locator = self.locators.get("email_field")
            password_field_locator = self.locators.get("password_field")
            login_button_locator = self.locators.get("login_button")

            if not email_field_locator or not password_field_locator or not login_button_locator:
                self.logger.error("❌ Missing locators for login fields.")
                raise KeyError("❌ Missing locators for login fields.")

            self.send_keys(email_field_locator, email)
            self.send_keys(password_field_locator, password)
            self.wait_for_element(login_button_locator)
            self.click(login_button_locator)
            self.logger.info("✅ Login button clicked successfully.")
        except Exception as e:
            self.logger.error(f"❌ Error while logging in: {e}", exc_info=True)
            raise

    def login_with_invalid_data(self, email, password):
        """Perform login with invalid credentials."""
        self.login(email, password, expect_failure=True)

        raise

    def click_on_signin_btn(self):
        self.click(self.locators.get("login_button"))

    def assert_login_texts(self):
        strings = StringsEn().LoginPage

        locators = {
            "title": self.locators.get("title"),  # Image
            "sub_title": self.locators.get("sub_title"),
            "email_field": self.locators.get("email_field"),
            "password_field": self.locators.get("password_field"),
            "reset_your_password_btn": self.locators.get("reset_your_password_btn"),
            "show_btn": self.locators.get("show_btn"),
            "login_button": self.locators.get("login_button"),
            "bottom_txt": self.locators.get("bottom_txt")
        }

        expected_texts = {
            "sub_title": strings.subtitle,
            "email_field": strings.email_placeholder,
            "password_field": strings.password_placeholder,
            "reset_your_password_btn": strings.reset_your_password,
            "show_btn": strings.show_btn,  # Only used if it's a text button (iOS)
            "login_button": strings.sign_in_btn,
            "bottom_txt": strings.bottom_txt
        }

        for element, locator in locators.items():
            if not locator:
                self.logger.warning(f"⚠️ Locator for '{element}' is missing, skipping...")
                continue

            if element == "title":  # Image assertion
                self.logger.info(f"🔍 Asserting visibility for '{element}' (image)")
                self.assert_visible(locator)

            elif element == "show_btn":
                if self.platform.lower() == "ios":  # iOS: Assert text
                    expected_text = expected_texts[element]
                    self.logger.info(f"🔍 Asserting text for '{element}' (iOS) -> Expected: '{expected_text}'")
                    self.assert_text(locator, expected_text)
                else:  # Android: Assert visibility (Icon)
                    self.logger.info(f"🔍 Asserting visibility for '{element}' (Android icon)")
                    self.assert_visible(locator)

            else:  # Other text elements
                expected_text = expected_texts[element]
                self.logger.info(f"🔍 Asserting text for '{element}' -> Expected: '{expected_text}'")
                self.assert_text(locator, expected_text)

        self.logger.info("✅ All login page elements (text + image) asserted successfully!")




