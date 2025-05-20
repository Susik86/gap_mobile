import time
import pytest
from other.logger import logger
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.Genius_Meter.GM_page import GMPage
from data.static.users import Users
from data.static.strings.en import StringsEn

@pytest.mark.usefixtures("driver")
class TestLoginUITests:
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
    def test_all_elements_have_appropriate_texts(self):
        self.logger.info("🚀 Starting test: test_all_elements_have_appropriate_texts")

        try:
            self.logger.info("🔍 Verifying that all login page elements have appropriate texts...")
            self.login_page.assert_login_texts()
            self.logger.info("✅ All elements have the correct text!")
        except AssertionError as e:
            self.logger.error(f"❌ Test failed due to assertion error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"❌ Test failed due to unexpected error: {e}")
            raise
        finally:
            self.logger.info("🛑 Test execution completed: test_all_elements_have_appropriate_texts")