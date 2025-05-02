# import logging
# import os
# from appium import webdriver
# from appium.options.android import UiAutomator2Options  # ✅ Import AppiumOptions
# from appium.options.ios import XCUITestOptions
# from selenium.common.exceptions import WebDriverException
# from config.config import CONFIG
#
# # Use an environment variable for flexibility
# APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723/wd/hub")
# print("@@22 APPIUM_SERVER_URL:", APPIUM_SERVER_URL)
#
# def get_driver(platform):
#     """Initialize and return the Appium driver for the given platform."""
#
#     logging.info(f"🔍 Available CONFIG keys: {CONFIG.keys()}")
#     logging.info(f"🔍 APPIUM_SERVER_URL: {APPIUM_SERVER_URL}")
#
#     logging.info(f"🔍 Checking CONFIG for platform: {platform}")
#     capabilities = CONFIG.get(platform)
#     logging.info(f"🔍 Retrieved Capabilities: {capabilities}")
#
#     if not capabilities:
#         logging.error(f"❌ No capabilities found for platform: {platform}. Check CONFIG!")
#         raise ValueError(f"❌ No capabilities found for platform: {platform}")
#
#     logging.info(f"🚀 Starting Appium driver for {platform} with capabilities: {capabilities}")
#
#     try:
#         # ✅ Convert capabilities into `AppiumOptions`
#         if platform == "android":
#             options = UiAutomator2Options()
#         elif platform == "ios":
#             options = XCUITestOptions()
#         else:
#             raise ValueError(f"❌ Unsupported platform: {platform}")
#
#         options.load_capabilities(capabilities)  # ✅ Load capabilities correctly
#
#         driver = webdriver.Remote(command_executor=APPIUM_SERVER_URL, options=options)
#         logging.info("✅ Driver started successfully!")
#         return driver
#
#     except WebDriverException as e:  # ✅ Correctly catching connection errors
#         logging.error(f"❌ Failed to connect to Appium server at {APPIUM_SERVER_URL}. Is Appium running?")
#         logging.error(f"🔍 Error Details: {e}")
#         raise
#
#     except Exception as e:
#         logging.error(f"❌ Unexpected error while starting Appium driver: {e}")
#         raise

import logging
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium.common.exceptions import WebDriverException
from config.config import CONFIG

def get_driver(platform: str):
    """Initialize and return the Appium driver for the given platform."""

    logging.info(f"🔍 Requested platform: {platform}")
    capabilities = CONFIG.get(platform)

    if not capabilities:
        raise ValueError(f"❌ No capabilities defined for platform: {platform}")

    # ✅ Move this out of try so it's always defined
    server_url = capabilities.get("server_url", "http://hub.browserstack.com/wd/hub")
    # if "127.0.0.1" in server_url:
    #     raise RuntimeError("❌ You are trying to run on local Appium instead of BrowserStack!")

    logging.info(f"📡 Using Appium server: {server_url}")

    try:
        logging.info(f"📦 Capabilities for {platform}: {capabilities}")

        if platform.lower() == "android":
            options = UiAutomator2Options()
        elif platform.lower() == "ios":
            options = XCUITestOptions()
        else:
            raise ValueError(f"❌ Unsupported platform: {platform}")

        options.load_capabilities(capabilities)

        driver = webdriver.Remote(
            command_executor=server_url,
            options=options
        )

        logging.info("✅ WebDriver started successfully!")
        return driver

    except WebDriverException as e:
        logging.error(f"❌ WebDriverException: Unable to connect to Appium server at {server_url}")
        logging.error(f"🔍 Details: {e}")
        raise

    except Exception as e:
        logging.error(f"❌ Unexpected error during driver initialization: {e}", exc_info=True)
        raise
