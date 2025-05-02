import logging
from data.locators.Genius_Meter_locators.GM_locators import GMLocators

from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class GMPage(BasePage):
    def __init__(self, driver, platform):
        super().__init__(driver)
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger

        self.platform = platform  # ✅ Store platform
        self.locators = GMLocators.get_locators("GM_PAGE", platform)  # ✅ Ensure platform is passed

        if not self.locators:
            self.logger.error(f"❌ No locators found for platform: {platform}")
            raise ValueError(f"❌ No locators found for platform: {platform}")


    def scroll_GM_screen_to_bottom(self):
        self.logger.info("🔹 Scrolling to the bottom of the GM page...")

        locators = GMLocators.get_locators("GM_PAGE", self.platform)
        self.scroll_until_visible("create_team_btn", self.platform, locators)

        self.logger.info("✅ Reached the bottom of the GM page.")


    def click_create_team_tab(self):
        """Clicks on the GM tab button."""
        try:
            create_team_btn = self.locators.get("create_team_btn")  # ✅ Get the locator
            if not create_team_btn:
                self.logger.error("❌ 'create_team_btn' locator is missing.")
                raise ValueError("❌ 'create_team_btn' locator is missing.")

            self.logger.info("🔹 Clicking Create a team...")
            self.click(create_team_btn)  # ✅ Use BasePage.click() method
            self.logger.info("✅ Create a team is clicked successfully!")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Create a team could not be clicked: {str(e)}")

            # 📸 Capture a screenshot for debugging
            screenshot_path = "logs/Create a team_not_clicked.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot saved: {screenshot_path}")

            raise AssertionError("❌ Create a team was not clickable.")