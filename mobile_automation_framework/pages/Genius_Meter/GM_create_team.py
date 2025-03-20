import logging
from data.locators.Genius_Meter_locators import GM_create_team_locators
from data.locators.Genius_Meter_locators.GM_create_team_locators import GMCreateTeamLocators
from data.static.strings.en import StringsEn

from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class GMCreateTeamPage(BasePage):
    def __init__(self, driver, platform):
        super().__init__(driver)
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger

        self.platform = platform  # ✅ Store platform
        self.locators = GMCreateTeamLocators.get_locators("GM_CREATE_TEAM_PAGE", platform)  # ✅ Ensure platform is passed

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
