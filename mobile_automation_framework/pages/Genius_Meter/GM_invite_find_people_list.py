import logging
import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from data.locators.Genius_Meter_locators.GM_invite_find_people_locators import GMInviteFindPeopleLocators
from data.locators.Genius_Meter_locators.GM_invite_to_team_locators import GMInviteToTeamTeamLocators
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class GMInviteFindPeoplePage(BasePage):
    def __init__(self, driver, platform):
        super().__init__(driver)
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger

        self.platform = platform  # ✅ Store platform
        self.locators = GMInviteFindPeopleLocators.get_locators("GM_PAGE", platform)  # ✅ Ensure platform is passed

        if not self.locators:
            self.logger.error(f"❌ No locators found for platform: {platform}")
            raise ValueError(f"❌ No locators found for platform: {platform}")



    def click_invite_button(self):
        """Clicks on the Invite button."""
        try:
            invite_btn = self.locators.get("add_members_btn")
            if not invite_btn:
                self.logger.error("❌ 'invite_btn' locator is missing.")
                raise ValueError("❌ 'invite_btn' locator is missing.")

            self.logger.info("🔹 Clicking Create invite_btn...")
            self.click(invite_btn)  # ✅ Use BasePage.click() method
            self.logger.info("✅ Invite button is clicked successfully!")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Invite button could not be clicked: {str(e)}")

            # 📸 Capture a screenshot for debugging
            screenshot_path = "logs/invite_btn_not_clicked.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot saved: {screenshot_path}")

            raise AssertionError("❌ Invite button was not clickable.")

    # def search_user_from_list(self, test_data):
    #     # self.logger.info("📝 Filling out GM team creation fields...")
    #
    #     search_field = self.locators.get("search_field")
    #     invite_button = self.locators.get("invite_button")
    #
    #
    #     # self.logger.info(f"🔹 Entering team name: {test_data['team_name_field']}")
    #     self.click(search_field)
    #     self.send_keys(search_field, "anahit arustamyan")
    #     # self.logger.info(f"🔹 Entering project name: {test_data['project_name_field']}")
    #     time.sleep(3)
    #     self.click(invite_button)

    def search_user_from_list(self, username: str, timeout: int = 15):
        """
        Types a username in the search box, hides the keyboard,
        and waits up to `timeout` seconds for the user result to appear in the list.
        """
        self.logger.info(f"🔍 Searching for user: '{username}'")

        search_box = self.locators.get("search_field")
        if not search_box:
            raise ValueError("❌ 'search_field' locator is missing.")

        # ✅ Focus and type in search
          # let the screen fully load


        self.send_keys(search_box, username)
        time.sleep(3)
        # self.hide_keyboard()

        self.logger.info("⏳ Waiting for user to appear in search results...")

        # ✅ Choose locator by platform
        platform = self.driver.capabilities.get("platformName", "").lower()
        if platform == "android":
            result_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{username}")')
        elif platform == "ios":
            result_locator = (AppiumBy.IOS_PREDICATE, f'label CONTAINS "{username}" OR name CONTAINS "{username}"')
        else:
            raise ValueError(f"❌ Unsupported platform: {platform}")

        try:
            result_element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(result_locator)
            )
            self.logger.info(f"✅ Found user result for '{username}'")
            return result_element

        except TimeoutException:
            self.logger.error(f"❌ User '{username}' not found within {timeout} seconds.")
            raise

    # def search_user_from_list_and_click_invite(self, username, timeout=10):
    #     """
    #     Searches for a user by name, then finds and clicks the Invite button next to that user.
    #     """
    #     self.logger.info(f"🔍 Searching and inviting user: '{username}'")
    #
    #     # Step 1: Locate and fill the search box
    #     search_box = self.locators.get("search_field")
    #     if not search_box:
    #         raise ValueError("❌ 'search_field' locator not defined.")
    #
    #     WebDriverWait(self.driver, timeout).until(
    #         EC.presence_of_element_located(search_box)
    #     ).send_keys(username)
    #
    #     self.logger.info(f"✅ Entered '{username}' in search field.")
    #
    #     # Step 2: Wait for the row that includes the username
    #     platform = self.driver.capabilities.get("platformName", "").lower()
    #
    #     if platform == "android":
    #         user_row_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{username}")')
    #     elif platform == "ios":
    #         user_row_locator = (AppiumBy.IOS_PREDICATE, f'label CONTAINS "{username}" OR name CONTAINS "{username}"')
    #     else:
    #         raise ValueError(f"❌ Unsupported platform: {platform}")
    #
    #     WebDriverWait(self.driver, timeout).until(
    #         EC.visibility_of_element_located(user_row_locator)
    #     )
    #
    #     self.logger.info(f"✅ Found row for user: {username}")
    #
    #     # Step 3: Find the Invite button near that user row
    #     if platform == "android":
    #         # A simple way: find all invite buttons and match by sibling text
    #         invite_buttons = self.driver.find_elements(AppiumBy.ID, "com.gapinternational.genius.qa:id/inviteButton")
    #     elif platform == "ios":
    #         # You may need to adjust this locator depending on button label
    #         invite_buttons = self.driver.find_elements(AppiumBy.IOS_PREDICATE, 'label == "Invite"')
    #
    #     for btn in invite_buttons:
    #         try:
    #             parent = btn.find_element(By.XPATH, "..")
    #             if username.lower() in parent.text.lower():
    #                 self.logger.info(f"👉 Tapping Invite for user: {username}")
    #                 btn.click()
    #                 self.logger.info("✅ Invite sent.")
    #                 return
    #         except Exception:
    #             continue
    #
    #     self.logger.error(f"❌ Invite button for '{username}' not found or not clickable.")
    #     raise AssertionError(f"Invite button for '{username}' not found.")


    # def assert_invite_to_team_screen_is_visible(self):
    #     self.logger.info("🔍 Asserting 'Invite to Team' screen is visible...")
    #
    #     # Define the locator (you can also store this in your locators dictionary)
    #     screen_title_locator = self.locators.get("done_btn")
    #
    #     try:
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.visibility_of_element_located(title_locator)
    #         )
    #         assert element.is_displayed(), "❌ 'Invite to Team' title is not visible!"
    #         self.logger.info("✅ 'Invite to Team' screen is visible.")
    #     except Exception as e:
    #         self.logger.error(f"❌ 'Invite to Team' screen not visible: {e}")
    #         raise AssertionError(f"'Invite to Team' screen not visible: {e}")
