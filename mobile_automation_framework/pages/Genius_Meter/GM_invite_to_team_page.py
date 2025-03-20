import logging
from data.locators.Genius_Meter_locators.GM_locators import GMLocators

from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class GMInviteToTeamPage(BasePage):
    def __init__(self, driver, platform):
        super().__init__(driver)
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger

        self.platform = platform  # ✅ Store platform
        self.locators = GMLocators.get_locators("GM_PAGE", platform)  # ✅ Ensure platform is passed

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