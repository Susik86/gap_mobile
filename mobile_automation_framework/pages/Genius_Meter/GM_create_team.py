import logging
import time
from telnetlib import EC

from data.locators.Genius_Meter_locators import GM_create_team_locators
from data.locators.Genius_Meter_locators.GM_create_team_locators import GMCreateTeamLocators
from data.static.GM_data import GM_data
from data.static.strings.en import StringsEn
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class GMCreateTeamPage(BasePage):
    def __init__(self, driver, platform):
        super().__init__(driver)
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger

        self.platform = platform  # ✅ Store platform
        self.locators = GMCreateTeamLocators.get_locators("GM_PAGE", platform)  # ✅ Ensure platform is passed

        if not self.locators:
            self.logger.error(f"❌ No locators found for platform: {platform}")
            raise ValueError(f"❌ No locators found for platform: {platform}")


    def assert_create_team_screen_is_visible(self):
        """Asserts that the "Create a team" screen is visible."""
        try:
            create_team_title = self.locators.get("screen_title")  # ✅ Get the locator
            self.wait_for_element(create_team_title, timeout=10)
            if not create_team_title:
                self.logger.error("❌ 'create_team_title' locator is missing.")
                raise ValueError("❌ 'create_team_title' locator is missing.")

            element = self.driver.find_element(*create_team_title)
            assert element.is_displayed(), "❌ Create a team screen is not visible!"

            self.logger.info("✅ create_team_title is visible on the Create a team screen.")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Create a team title is NOT visible: {str(e)}")

            # 📸 Capture a screenshot
            screenshot_path = "logs/Create_a_team_is_not_visible.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot saved: {screenshot_path}")

            raise AssertionError("❌ Create a team title was not found.")

    def assert_create_team_screen_texts(self):
        strings = StringsEn().GMCreateTeamPage
        string_general = StringsEn().General


        locators = {
            "title": self.locators.get("screen_title"),
            "team_name_field": self.locators.get("team_name_field"),
            "project_name_field": self.locators.get("project_name_field"),
            "outcome_field": self.locators.get("outcome_field"),
            "submit_btn": self.locators.get("submit_btn"),
            "cancel_btn": self.locators.get("cancel_btn"),
            "back_button":self.locators.get("back_button"),
            "legend_icon":self.locators.get("legend_icon"),

        }

        expected_texts = {
            "title": strings.title,
            "team_name_field": strings.team_name,
            "project_name_field": strings.project_name,
            "outcome_field": strings.outcome_name,
            "submit_btn": string_general.submit_btn,
            "cancel_btn":string_general.cancel_btn

        }

        for element, locator in locators.items():
            if not locator:
                self.logger.warning(f"⚠️ Locator for '{element}' is missing, skipping...")
                continue

            if element in ["back_button", "legend_icon"]:  # ✅ Corrected condition
                self.logger.info(f"🔍 Asserting visibility for '{element}' (image)")
                self.assert_visible(locator)

            else:  # Other text elements
                expected_text = expected_texts.get(element, None)
                if expected_text:
                    self.logger.info(f"🔍 Asserting text for '{element}' -> Expected: '{expected_text}'")
                    self.assert_text(locator, expected_text)
                else:
                    self.logger.warning(f"⚠️ No expected text found for '{element}', skipping assertion.")

        self.logger.info("✅ All create team screen elements (text + image) asserted successfully!")


    def fill_create_GM_team_fields(self, test_data):
        """
        Fills the GM team creation form with data from test_data dict.
        Expected keys: 'team_name_field', 'project_name_field', 'outcome_field'
        """
        self.logger.info("📝 Filling out GM team creation fields with:")
        self.logger.info(f"   • Team Name: {test_data['team_name_field']}")
        self.logger.info(f"   • Project Name: {test_data['project_name_field']}")
        self.logger.info(f"   • Outcome: {test_data['outcome_field']}")

        # ✅ Get locators
        team_field = self.locators.get("team_name_field")
        team_field_clicked = self.locators.get("team_name_field_clicked")
        project_field = self.locators.get("project_name_field")
        project_field_clicked = self.locators.get("project_name_field_clicked")
        outcome_field = self.locators.get("outcome_field")
        outcome_field_clicked = self.locators.get("outcome_field_clicked")

        # ✅ Fill Team Name
        self.logger.info("🔹 Focusing and typing into Team Name field...")
        self.click(team_field)
        self.send_keys( team_field_clicked, test_data["team_name_field"])

        # ✅ Fill Project Name
        self.logger.info("🔹 Focusing and typing into Project Name field...")
        self.click(project_field)
        self.send_keys(project_field_clicked, test_data["project_name_field"])

        # ✅ Fill Outcome
        self.logger.info("🔹 Focusing and typing into Outcome field...")
        self.click(outcome_field)
        self.send_keys(outcome_field_clicked, test_data["outcome_field"])
        self.logger.info("✅ GM team form filled successfully.")


    def assert_create_GM_fields_filled_correctly(self, expected_data):
        self.logger.info("🔍 Asserting values in GM form fields...")

        # Get locators
        team_name_locator = self.locators.get("team_name_field")
        project_name_locator = self.locators.get("project_name_field")
        outcome_name_locator = self.locators.get("outcome_field")

        # Get actual values from fields
        actual_team_name = self.get_element_value(team_name_locator)
        actual_project_name = self.get_element_value(project_name_locator)
        actual_outcome_name = self.get_element_value(outcome_name_locator)

        # Assertions
        assert actual_team_name == expected_data["team_name_field"], \
            f"❌ Team name mismatch: Expected '{expected_data['team_name_field']}', got '{actual_team_name}'"

        assert actual_project_name == expected_data["project_name_field"], \
            f"❌ Project name mismatch: Expected '{expected_data['project_name_field']}', got '{actual_project_name}'"

        assert actual_outcome_name == expected_data["outcome_field"], \
            f"❌ Outcome name mismatch: Expected '{expected_data['outcome_field']}', got '{actual_outcome_name}'"

        self.logger.info("✅ All GM form fields are filled and verified correctly.")


    def click_on_submit_btn(self, timeout=10):
        """Clicks the Submit button on the Create Team screen with waits and logs."""
        submit_btn_locator = self.locators.get("submit_btn")

        if not submit_btn_locator:
            self.logger.error("❌ 'submit_btn' locator is missing.")
            raise ValueError("❌ 'submit_btn' locator is missing.")

        try:
            self.logger.info("⏳ Waiting for 'Submit' button to be visible...")
            element = self.wait.until(EC.visibility_of_element_located(submit_btn_locator))
            self.logger.info("✅ 'Submit' button is visible. Clicking now...")
            element.click()
            self.logger.info("✅ 'Submit' button clicked successfully.")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Failed to click Submit button: {e}")
            screenshot_path = "logs/submit_click_failed.png"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"📸 Screenshot saved: {screenshot_path}")
            raise
