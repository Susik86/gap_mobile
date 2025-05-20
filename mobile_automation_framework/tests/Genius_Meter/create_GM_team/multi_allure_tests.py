import time
import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from data.static.users import Users
from data.static.strings.en import StringsEn
from other.logger import logger
from utils.allure_steps import attach_screenshot, attach_log
from utils.push_helper import PushHelper
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.Genius_Meter.GM_page import GMPage
from pages.Genius_Meter.GM_create_team import GMCreateTeamPage
from pages.Genius_Meter.GM_invite_to_team_page import GMInviteToTeamPage
from pages.Genius_Meter.GM_invite_find_people_list import GMInviteFindPeoplePage


def get_platform_name(driver):
    caps = driver.capabilities
    return caps.get("platformName") or caps.get("appium:platformName") or "Unknown"


class TestCreateGMTeamSuccessfully:

    @pytest.fixture(autouse=True)
    def setup(self, multidevice_drivers):
        self.logger = logger
        self.driver_ios, self.driver_android = multidevice_drivers
        self.platform_ios = get_platform_name(self.driver_ios)
        self.platform_android = get_platform_name(self.driver_android)

        self.logger.info("🔹 Setting up Multi-Device GM Team Test")
        self.logger.info(f"📱 iOS: {self.platform_ios} | 🤖 Android: {self.platform_android}")

        user_a = Users.get_user_a()
        self.login_page_ios = LoginPage(self.driver_ios, self.platform_ios)
        self.dashboard_page_ios = DashboardPage(self.driver_ios, self.platform_ios)
        self.gm_page_ios = GMPage(self.driver_ios, self.platform_ios)
        self.create_GM_screen_ios = GMCreateTeamPage(self.driver_ios, self.platform_ios)
        self.create_GM_Invite_Members_screen_ios = GMInviteToTeamPage(self.driver_ios, self.platform_ios)
        self.GM_Invite_find_people_screen_ios = GMInviteFindPeoplePage(self.driver_ios, self.platform_ios)

        self.login_page_ios.open_app()
        self.logger.info(f"🔐 Logging in User A (iOS): {user_a['email']}")
        self.login_page_ios.login(user_a["email"], user_a["password"])
        self.dashboard_page_ios.assert_dashboard_tab_is_visible()

        user_b = Users.get_user_b()
        self.login_page_android = LoginPage(self.driver_android, self.platform_android)
        self.dashboard_page_android = DashboardPage(self.driver_android, self.platform_android)

        self.login_page_android.open_app()
        self.logger.info(f"🔐 Logging in User B (Android): {user_b['email']}")
        self.login_page_android.login(user_b["email"], user_b["password"])
        self.dashboard_page_android.assert_dashboard_tab_is_visible()

        self.strings = StringsEn().LoginPage

    @pytest.mark.run
    def test_create_GM_team_successfully(self):
        """User A creates group ➜ User B receives push ➜ Group becomes visible."""

        self.dashboard_page_ios.click_gm_tab()
        time.sleep(2)

        self.dashboard_page_ios.click_by_visible_text("Launch Genius Pulse")
        time.sleep(2)
        self.dashboard_page_ios.click_alert_ok()

        self.logger.info("📱 Backgrounding User B app to prepare for push...")
        self.driver_android.background_app(12)

        self.logger.info("📲 Waiting for push notification...")
        expected_push_text = "New Genius Pulse launched.Tap now to take the Pulse."
        self.push_helper_android = PushHelper(platform="android")
        self.push_helper_android.wait_for_push_containing(expected_push_text, timeout=40)

        self.logger.info("🔔 Opening Android notification shade")
        self.driver_android.open_notifications()

        push_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("New Genius Pulse launched")'
        )
        notification = WebDriverWait(self.driver_android, 15).until(
            EC.presence_of_element_located(push_locator)
        )
        notification.click()
        self.logger.info("✅ Tapped push notification successfully")
        time.sleep(10)
        # Optional: Attach screenshots manually for success verification
        attach_screenshot(self.driver_ios, name="iOS_Success", folder="gm_team")
        attach_screenshot(self.driver_android, name="Android_Success", folder="gm_team")




        attach_log("Test Execution Log", "logs/test_execution.log")
