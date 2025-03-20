import os
import allure
import logging

from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class BasePage:
    def __init__(self, driver: WebDriver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)  # ✅ Default timeout
        self.logger = logging.getLogger("mobile_framework_logger")  # ✅ Use centralized logger

    def click(self, locator):
        """Wait for an element and click."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"✅ Clicked on {locator}")
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Failed to click element {locator}: {e}")
            raise

    def send_keys(self, locator, text):
        """Wait for an element and send keys."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            self.logger.info(f"✅ Sent keys to {locator}: {text}")
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Failed to send keys to {locator}: {e}")
            raise

    def wait_for_element(self, locator, timeout=15):
        """Wait for an element to be present and visible."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"❌ Timeout: {locator} not found")
            raise

    # def assert_popup_text(self, popup_locator, expected_text, timeout=10, partial_match=True):
    #     """Asserts that a pop-up appears and contains the expected text."""
    #     try:
    #         popup_element = self.wait_for_element(popup_locator, timeout=timeout)
    #         actual_text = popup_element.text.strip().lower()
    #         expected_text = expected_text.strip().lower()
    #
    #         self.logger.info(f"📌 Pop-up text found: '{actual_text}'")
    #
    #         if partial_match:
    #             assert expected_text in actual_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"
    #         else:
    #             assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"
    #
    #         self.logger.info("✅ Pop-up text assertion passed!")
    #
    #     except (TimeoutException, NoSuchElementException) as e:
    #         self.logger.error(f"❌ Pop-up not found or text mismatch: {str(e)}")
    #
    #         os.makedirs("logs", exist_ok=True)  # ✅ Ensure logs directory exists
    #
    #         screenshot_path = "logs/popup_not_visible.png"
    #         self.driver.save_screenshot(screenshot_path)
    #
    #         with open(screenshot_path, "rb") as image:
    #             allure.attach(image.read(), name="Popup Failure", attachment_type=allure.attachment_type.PNG)
    #
    #         raise AssertionError("❌ Pop-up was not found or did not contain the expected text")

    # def scroll_to_bottom(self, platform, button_locator=None, max_scrolls=15):
    #     """
    #     Dynamically scrolls to the bottom of the screen for iOS and Android.
    #     If a button locator is provided, scrolls until the button is visible.
    #     Prevents infinite loops by limiting the number of scrolls.
    #     """
    #     try:
    #         scroll_count = 0  # Counter to track number of scrolls
    #
    #         while scroll_count < max_scrolls:
    #             # ✅ Stop if the button becomes visible
    #             if button_locator:
    #                 try:
    #                     button = WebDriverWait(self.driver, 2).until(
    #                         EC.visibility_of_element_located(button_locator)
    #                     )
    #                     if button.is_displayed():
    #                         self.logger.info(f"✅ Button '{button_locator}' is now visible. Stopping scroll.")
    #                         break  # ✅ Stop scrolling when the button is found
    #                 except TimeoutException:
    #                     self.logger.info(f"🔄 '{button_locator}' not found yet, scrolling down...")
    #
    #             # Perform scrolling based on platform
    #             if platform.lower() == "ios":
    #                 self.logger.info("🔹 Scrolling down on iOS...")
    #                 self.driver.execute_script("mobile: swipe", {"direction": "up"})
    #
    #             elif platform.lower() == "android":
    #                 self.logger.info("🔹 Scrolling down on Android...")
    #                 self.driver.execute_script("mobile: scrollGesture", {
    #                     "left": 100, "top": 100, "width": 800, "height": 1600,
    #                     "direction": "down",
    #                     "percent": 3.0
    #                 })
    #             else:
    #                 raise ValueError(f"❌ Unsupported platform: {platform}")
    #
    #             time.sleep(1)  # Small delay to allow UI updates
    #             scroll_count += 1  # Increment scroll count
    #
    #         if scroll_count >= max_scrolls:
    #             self.logger.warning(f"⚠️ Max scroll attempts ({max_scrolls}) reached. Button might not be present.")
    #
    #         self.logger.info("✅ Scroll completed!")
    #
    #     except Exception as e:
    #         self.logger.error(f"❌ Failed to scroll: {str(e)}")
    #         raise


    def assert_text(self, locator, expected_text, timeout=10, partial_match=True):
        """
        Asserts that an element (pop-up or any UI element) contains the expected text.

        :param locator: Tuple (By strategy, locator string) to locate the element.
        :param expected_text: The expected text inside the element.
        :param timeout: Time to wait for the element (default: 10 seconds).
        :param partial_match: If True, checks if expected text is in actual text. If False, checks exact match.
        """
        try:
            # Wait for the element to be present and visible
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            actual_text = element.text.strip()

            self.logger.info(f"📌 Found text: '{actual_text}' in element {locator}")

            # Compare text based on full or partial match
            if partial_match:
                assert expected_text.lower() in actual_text.lower(), f"❌ Expected '{expected_text}', but got '{actual_text}'"
            else:
                assert actual_text.lower() == expected_text.lower(), f"❌ Expected '{expected_text}', but got '{actual_text}'"

            self.logger.info("✅ Text assertion passed!")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"❌ Element not found or text mismatch: {e}")

            # Capture screenshot for debugging
            os.makedirs("logs", exist_ok=True)
            screenshot_path = f"logs/assertion_failure.png"
            self.driver.save_screenshot(screenshot_path)

            with open(screenshot_path, "rb") as image:
                allure.attach(image.read(), name="Assertion Failure", attachment_type=allure.attachment_type.PNG)

            raise AssertionError(f"❌ Assertion failed: Expected '{expected_text}' but element was missing or text did not match.")


    def scroll_to_bottom(self, platform, button_locator=None, max_scrolls=2):
        try:
            scroll_count = 0  # Counter to track number of scrolls

            while scroll_count < max_scrolls:
                if button_locator:
                    try:
                        button = WebDriverWait(self.driver, 2).until(
                            EC.visibility_of_element_located(button_locator)
                        )
                        if button.is_displayed():
                            self.logger.info(f"✅ Button '{button_locator}' is now visible. Stopping scroll.")
                            # button.click()  # Ensure the button is clicked once found
                            break  # ✅ Stop scrolling when the button is found
                    except TimeoutException:
                        self.logger.info(f"🔄 '{button_locator}' not found yet, scrolling down...")

                # Perform scrolling based on platform
                if platform.lower() == "ios":
                    self.logger.info("🔹 Scrolling down on iOS...")
                    self.driver.execute_script("mobile: swipe", {"direction": "up"})

                elif platform.lower() == "android":
                    self.logger.info("🔹 Scrolling down on Android...")

                    # Try swiping first
                    try:
                        self.driver.execute_script("mobile: swipe", {"direction": "up"})
                    except Exception:
                        self.logger.info("⚠️ Swipe failed, trying scrollGesture...")

                        # If swipe fails, fall back to scrollGesture with increased percent
                        try:
                            self.driver.execute_script("mobile: scrollGesture", {
                                "left": 100, "top": 100, "width": 800, "height": 1600,
                                "direction": "down",
                                "percent": 80  # Increased percent for better visibility
                            })
                        except Exception as e:
                            self.logger.error(f"❌ Scrolling failed: {e}")

                else:
                    raise ValueError(f"❌ Unsupported platform: {platform}")

                time.sleep(1)  # Small delay to allow UI updates
                scroll_count += 1  # Increment scroll count

            if scroll_count >= max_scrolls:
                self.logger.warning(f"⚠️ Max scroll attempts ({max_scrolls}) reached. Button might not be present.")
                print(self.driver.page_source)  # Dump page source for debugging

            self.logger.info("✅ Scroll completed!")

        except Exception as e:
            self.logger.error(f"❌ Failed to scroll: {str(e)}")
            raise

    # def scroll_to_bottom(self, platform, button_locator):
    #     try:
    #         self.logger.info("🔹 Checking if button is already visible...")
    #
    #         # ✅ Check if the button is visible BEFORE scrolling
    #         try:
    #             button = WebDriverWait(self.driver, 2).until(
    #                 EC.visibility_of_element_located(button_locator)
    #             )
    #             if button.is_displayed():
    #                 self.logger.info(f"✅ Button '{button_locator[1]}' is already visible. Clicking it now.")
    #                 button.click()  # ✅ Click immediately if visible
    #                 return  # ✅ Stop execution
    #         except TimeoutException:
    #             self.logger.info(f"🔄 '{button_locator[1]}' not visible yet, attempting a scroll...")
    #
    #         # 🔄 If not visible, perform ONE scroll
    #         self.logger.info("🔄 Scrolling once to check if button appears...")
    #         if platform.lower() == "ios":
    #             self.driver.execute_script("mobile: swipe", {"direction": "up"})
    #         elif platform.lower() == "android":
    #             try:
    #                 self.driver.execute_script("mobile: swipe", {"direction": "up"})
    #             except Exception:
    #                 self.driver.execute_script("mobile: scrollGesture", {
    #                     "left": 100, "top": 100, "width": 800, "height": 1600,
    #                     "direction": "down",
    #                     "percent": 80
    #                 })
    #         else:
    #             raise ValueError(f"❌ Unsupported platform: {platform}")
    #
    #         time.sleep(1)  # Small delay for UI to update
    #
    #         # ✅ Check if the button is visible again after scrolling
    #         try:
    #             button = WebDriverWait(self.driver, 3).until(
    #                 EC.visibility_of_element_located(button_locator)
    #             )
    #             if button.is_displayed():
    #                 self.logger.info(f"✅ Button '{button_locator[1]}' is now visible after scrolling. Clicking it now.")
    #                 button.click()  # ✅ Click the button after one scroll
    #                 return  # ✅ Stop execution
    #         except TimeoutException:
    #             self.logger.warning(f"⚠️ Button '{button_locator[1]}' still not visible after one scroll.")
    #
    #     except Exception as e:
    #         self.logger.error(f"❌ Failed to scroll and find button: {str(e)}")
    #         raise



    def swipe(self, direction, duration=800, repeat=1):
        """
        Swipes the screen multiple times in the given direction (left, right).

        :param direction: "left", "right"
        :param duration: Time in milliseconds for the swipe action (default: 800)
        :param repeat: Number of times to repeat the swipe (default: 1)
        """
        size = self.driver.get_window_size()
        width, height = size["width"], size["height"]

        if direction == "left":
            start_x, start_y, end_x, end_y = width * 0.8, height / 2, width * 0.2, height / 2
        elif direction == "right":
            start_x, start_y, end_x, end_y = width * 0.2, height / 2, width * 0.8, height / 2
        else:
            raise ValueError(f"❌ Invalid direction: {direction}. Use 'left' or 'right'.")

        for _ in range(repeat):  # Repeat swiping 'repeat' times
            # ✅ Define touch input (Use "touch" instead of PointerInput.TOUCH)
            finger = PointerInput("touch", "finger")

            # ✅ Create action builder and add pointer input
            actions = ActionBuilder(self.driver)
            actions.add_pointer_input("touch", "finger")  # ✅ Correct


            # Swipe sequence
            actions.pointer_action \
                .move_to_location(start_x, start_y) \
                .pointer_down() \
                .pause(duration / 1000) \
                .move_to_location(end_x, end_y) \
                .pointer_up()

            # Execute the action
            actions.perform()

            print(f"✅ Swiped {direction} ({_+1}/{repeat})")


    def assert_visible(self, locator, timeout=10):
        """
        Asserts that an element (image, button, text, etc.) is visible.

        :param locator: Tuple (By strategy, locator string) to locate the element.
        :param timeout: Time to wait for the element (default: 10 seconds).
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            assert element.is_displayed(), f"❌ Element {locator} is not visible!"
            self.logger.info(f"✅ Element {locator} is visible!")
        except TimeoutException:
            self.logger.error(f"❌ Timeout: Element {locator} not visible!")
            raise AssertionError(f"❌ Element {locator} is not visible!")





