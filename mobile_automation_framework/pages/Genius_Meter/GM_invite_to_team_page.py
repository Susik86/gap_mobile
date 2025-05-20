import logging

from selenium.webdriver.support.wait import WebDriverWait

from data.locators.Genius_Meter_locators.GM_invite_to_team_locators import GMInviteToTeamTeamLocators

from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class GMInviteToTeamPage(BasePage):
    def __init__(self, driver, platform):
        super().__init__(driver)
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger

        self.platform = platform  # ✅ Store platform
        self.locators = GMInviteToTeamTeamLocators.get_locators("GM_PAGE", platform)  # ✅ Ensure platform is passed

        if not self.locators:
            self.logger.error(f"❌ No locators found for platform: {platform}")
            raise ValueError(f"❌ No locators found for platform: {platform}")

    def click_done_tab(self):
        """Clicks on the GM tab button."""
        try:
            done_btn = self.locators.get("done_btn")
            if not done_btn:
                self.logger.error("❌ 'create_team_btn' locator is missing.")
                raise ValueError("❌ 'create_team_btn' locator is missing.")

            self.logger.info("🔹 Clicking Create a team...")
            self.click(done_btn)  # ✅ Use BasePage.click() method
            self.logger.info("✅ Done button is clicked successfully!")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ DOne button could not be clicked: {str(e)}")

            # 📸 Capture a screenshot for debugging
            screenshot_path = "logs/done_btn_not_clicked.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot saved: {screenshot_path}")

            raise AssertionError("❌ Done button was not clickable.")

    def click_add_members_button(self):
        """Clicks on the Add members button."""
        try:
            add_members_btn = self.locators.get("add_members_btn")
            if not add_members_btn:
                self.logger.error("❌ 'add_members_btn' locator is missing.")
                raise ValueError("❌ 'add_members_btn' locator is missing.")

            self.logger.info("🔹 Clicking Create add_members_btn...")
            self.click(add_members_btn)  # ✅ Use BasePage.click() method
            self.logger.info("✅ Add Members button is clicked successfully!")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Add Members button could not be clicked: {str(e)}")

            # 📸 Capture a screenshot for debugging
            screenshot_path = "logs/add_members_btn_not_clicked.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot saved: {screenshot_path}")

            raise AssertionError("❌ Done button was not clickable.")



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
