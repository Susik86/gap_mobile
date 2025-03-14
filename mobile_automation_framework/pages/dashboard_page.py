import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from data.locators.dashboard_locators import DashboardLocators
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class DashboardPage(BasePage):
    def __init__(self, driver, platform):
        super().__init__(driver)
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger

        self.platform = platform  # ✅ Store platform
        self.locators = DashboardLocators.get_locators("DASHBOARD_PAGE", platform)  # ✅ Ensure platform is passed

        if not self.locators:
            self.logger.error(f"❌ No locators found for platform: {platform}")
            raise ValueError(f"❌ No locators found for platform: {platform}")

    def assert_dashboard_tab_is_visible(self):
        """Asserts that the Dashboard tab is visible after login."""
        try:
            dashboard_tab = self.locators.get("dashboard_tab_btn")
            self.wait_for_element(dashboard_tab, timeout=10)
            print("Trying to locate:", dashboard_tab)  # Debugging print
            if not dashboard_tab:
                self.logger.error("❌ 'dashboard_tab_btn' locator is missing.")
                raise ValueError("❌ 'dashboard_tab_btn' locator is missing.")

            element = self.driver.find_element(*dashboard_tab)
            assert element.is_displayed(), "❌ Dashboard tab is not visible!"

            self.logger.info("✅ Dashboard tab is visible on the Dashboard.")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Dashboard tab is NOT visible: {str(e)}")

            # 📸 Capture a screenshot
            screenshot_path = "logs/Dashboard_tab_not_visible.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot saved: {screenshot_path}")

            raise AssertionError("❌ Dashboard tab was not found.")

    def click_gm_tab(self):
        """Clicks on the GM tab button."""
        try:
            gm_tab = self.locators.get("gm_tab_btn")  # ✅ Get the locator
            if not gm_tab:
                self.logger.error("❌ 'gm_tab_btn' locator is missing.")
                raise ValueError("❌ 'gm_tab_btn' locator is missing.")

            self.logger.info("🔹 Clicking GM tab...")
            self.click(gm_tab)  # ✅ Use BasePage.click() method
            self.logger.info("✅ GM tab clicked successfully!")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ GM tab could not be clicked: {str(e)}")

            # 📸 Capture a screenshot for debugging
            screenshot_path = "logs/GM_tab_not_clicked.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot saved: {screenshot_path}")

            raise AssertionError("❌ GM tab was not clickable.")
