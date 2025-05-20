import time


import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from data.static.GM_data import GM_data
from other.logger import logger
from pages.Genius_Meter.GM_create_team import GMCreateTeamPage
from pages.Genius_Meter.GM_invite_find_people_list import GMInviteFindPeoplePage
from pages.Genius_Meter.GM_invite_to_team_page import GMInviteToTeamPage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.Genius_Meter.GM_page import GMPage
from data.static.users import Users
from data.static.strings.en import StringsEn
from utils.push_helper import PushHelper


# ✅ Platform name normalizer
def get_platform_name(driver):
    caps = driver.capabilities
    return caps.get("platformName") or caps.get("appium:platformName") or "Unknown"

class TestCreateGMTeamSuccessfully():

    @pytest.fixture(autouse=True)
    def setup(self, multidevice_drivers):
        """Setup for multi-device test using iOS (User A) and Android (User B)"""
        self.logger = logger
        self.logger.info("🔹 Setting up Multi-Device GM Team Test")

        # ✅ Drivers for iOS (User A) and Android (User B)
        self.driver_ios, self.driver_android = multidevice_drivers
        self.platform_ios = get_platform_name(self.driver_ios)
        self.platform_android = get_platform_name(self.driver_android)

        self.logger.info(f"📱 iOS Device Platform: {self.platform_ios}")
        self.logger.info(f"🤖 Android Device Platform: {self.platform_android}")

        # 👤 User A - iOS login
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

        # 👤 User B - Android login
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
        """Test flow: User A creates group ➜ User B receives push ➜ Group becomes visible."""

        # 👤 Step 1: User A (iOS) navigates and creates a group
        self.dashboard_page_ios.click_gm_tab()
        time.sleep(2)



        self.dashboard_page_ios.click_by_visible_text("Launch Genius Pulse")
        time.sleep(2)
        self.dashboard_page_ios.click_alert_ok()
        self.logger.info("📱 Backgrounding User B app to prepare for push...")
        self.driver_android.background_app(12)  # Background for 10 seconds




        # self.gm_page_ios.scroll_GM_screen_to_bottom()
        # self.gm_page_ios.click_create_team_tab()
        # self.create_GM_screen_ios.assert_create_team_screen_is_visible()

        # 📄 Generate group creation data
        # data = GM_data.get_random_create_GM_screen_data()
        #
        # self.create_GM_screen_ios.fill_create_GM_team_fields(data)
        # # self.create_GM_screen_ios.assert_create_GM_fields_filled_correctly(data)
        # self.create_GM_screen_ios.click_on_submit_btn()
        # time.sleep(3)
        # self.create_GM_Invite_Members_screen_ios.click_add_members_button()
        # username = self.GM_Invite_find_people_screen_ios.search_user_from_list("susanna karapetyan")
        # self.GM_Invite_find_people_screen_ios.tap(username)
        # self.GM_Invite_find_people_screen_ios.click_invite_button_for_user("susanna karapetyan")

        # 👤 Step 2: User B (Android) waits to receive push notification
        # expected_push_text = "You are invited to join a team. Tap now to join."


        # ✅ Step 1: Background the app so Android can show push
        self.logger.info("📲 Sending User B app to background...")
        self.driver_android.background_app(10)

        # ✅ Step 2: Wait for backend to confirm push sent
        expected_push_text = "New Genius Pulse launched.Tap now to take the Pulse."
        self.logger.info(f"📲 Waiting for push notification: '{expected_push_text}'")
        self.push_helper_android = PushHelper(platform="android")
        self.push_helper_android.wait_for_push_containing(expected_push_text, timeout=40)

        # ✅ Step 3: Open system notifications
        self.logger.info("🔔 Opening Android notification shade")
        self.driver_android.open_notifications()  # this calls your method

        # ✅ Step 4: Wait for and tap the notification
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


