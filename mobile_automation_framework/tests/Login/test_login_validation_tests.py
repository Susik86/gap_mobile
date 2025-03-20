import time
import pytest

from data.locators.login_locators import LoginLocators
from other.logger import logger
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.Genius_Meter.GM_page import GMPage
from data.static.users import Users
from data.static.strings.en import StringsEn

@pytest.mark.usefixtures("driver")
class TestLoginValidationTests:
    """ Test Class for login functionality """

    @pytest.fixture(autouse=True)
    def setup(self, driver, platform):
        """Setup before each test runs."""
        self.logger = logger
        self.logger.info("🔹 Setting up Login Test")

        self.driver = driver
        app_package = self.driver.capabilities.get("appPackage")

        if app_package:
            self.logger.info("🔄 Restarting App for a fresh session...")
            self.driver.terminate_app(app_package)
            self.driver.activate_app(app_package)

        self.platform = self.driver.capabilities.get("platformName", "Unknown")
        self.logger.info(f"🔍 Running on platform: {self.platform}")

        # Initialize page objects separately per test
        self.login_page = LoginPage(self.driver, self.platform)
        self.dashboard_page = DashboardPage(self.driver, self.platform)
        self.gm_page = GMPage(self.driver, self.platform)
        self.strings = StringsEn().LoginPage
        self.locators = LoginLocators.get_locators("LOGIN_PAGE", platform)
        self.login_page.open_app()


    # @pytest.mark.run
    # def test_invalid_login_pop_up(self):
    #     """ Perform login with invalid credentials and verify the pop-up message. """
    #     self.logger.info(f"🔹 Running invalid login test on: {self.platform}")
    #
    #     user = Users.get_random_invalid_user()
    #     email = user["email"]
    #     password = user["password"]
    #
    #     self.logger.info(f"🔐 Attempting login with invalid credentials: {email} / {password}")
    #
    #     self.login_page.login(email, password)
    #     self.login_page.assert_text(self.strings.invalid_login_pop_up)
    #     self.logger.info("✅ Login username or password is invalid pop-up is visible!")


    @pytest.mark.run
    def test_leaving_email_and_password_empty_results_in_required_field_error(self):
        required_email_error = self.locators.get("email_error")
        required_password_error = self.locators.get("password_error")

        self.logger.info(f"🔹 Running invalid login test on: {self.platform}")
        self.login_page.click_on_signin_btn()
        self.login_page.assert_text(required_email_error, self.strings.empty_email)
        self.login_page.assert_text(required_password_error, self.strings.empty_password)
        # self.logger.info("✅ ")
