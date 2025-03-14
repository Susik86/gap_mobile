import time
import pytest
from other.logger import logger
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.gm_page import GMPage
from data.static.users import Users
from data.static.strings.en import StringsEn

@pytest.mark.usefixtures("driver")
class TestValidLogin:
    """ Test Class for login functionality """

    @pytest.fixture(autouse=True)
    def setup(self, driver):
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
        self.login_page.open_app()


    @pytest.mark.run
    def test_valid_login(self):
        """ Perform login with valid credentials and verify the dashboard title. """
        self.logger.info(f"🔹 Running valid login test on: {self.platform}")

        user = Users.get_random_valid_user()
        email = user["email"]
        password = user["password"]

        self.logger.info(f"🔐 Logging in with: {email} / {password}")
        self.login_page.login(email, password)
        self.dashboard_page.assert_dashboard_tab_is_visible()
        self.dashboard_page.swipe("left", repeat=5)
        self.logger.info("✅ Login test completed successfully!")
