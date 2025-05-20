import logging
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium.common.exceptions import WebDriverException
from config.config import CONFIG

APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723/wd/hub")

def get_driver(platform, instance_name=None):
    """
    Initialize and return the Appium driver for the given platform.
    instance_name: Optional label for parallel/multi-user sessions (e.g., 'user_a', 'user_b')
    """

    logging.info(f"🔍 Checking CONFIG for platform: {platform}")
    base_caps = CONFIG.get(platform)

    if not base_caps:
        raise ValueError(f"❌ No capabilities found for platform: {platform}")

    # Copy caps to avoid mutating shared CONFIG
    capabilities = base_caps.copy()

    # Dynamic port overrides (for local parallel devices)
    if platform == "android":
        if instance_name == "user_b":
            capabilities["systemPort"] = 8202  # Ensure it's different
    elif platform == "ios":
        if instance_name == "user_a":
            capabilities["wdaLocalPort"] = 8101  # Use custom WDA port for parallel sim

    logging.info(f"🚀 Starting Appium driver for {platform} ({instance_name}) with capabilities: {capabilities}")

    try:
        if platform == "android":
            options = UiAutomator2Options()
        elif platform == "ios":
            options = XCUITestOptions()
        else:
            raise ValueError(f"❌ Unsupported platform: {platform}")

        options.load_capabilities(capabilities)

        driver = webdriver.Remote(command_executor=APPIUM_SERVER_URL, options=options)
        logging.info(f"✅ {platform.upper()} driver for {instance_name} started.")
        return driver

    except WebDriverException as e:
        logging.error(f"❌ Appium connection failed for {platform} ({instance_name})")
        logging.error(f"🔍 Error: {e}")
        raise

    except Exception as e:
        logging.error(f"❌ Unexpected error starting {platform} ({instance_name}) driver: {e}")
        raise


# import logging
# import os
# from appium import webdriver
# from appium.options.android import UiAutomator2Options
# from appium.options.ios import XCUITestOptions
# from selenium.common.exceptions import WebDriverException
# from config.config import CONFIG
#
# def get_driver(platform: str):
#     """Initialize and return the Appium driver for the given platform."""
#
#     logging.info(f"🔍 Requested platform: {platform}")
#     capabilities = CONFIG.get(platform)
#
#     if not capabilities:
#         raise ValueError(f"❌ No capabilities defined for platform: {platform}")
#
#     # ✅ Move this out of try so it's always defined
#     server_url = capabilities.get("server_url", "http://hub.browserstack.com/wd/hub")
#     # if "127.0.0.1" in server_url:
#     #     raise RuntimeError("❌ You are trying to run on local Appium instead of BrowserStack!")
#
#     logging.info(f"📡 Using Appium server: {server_url}")
#
#     try:
#         logging.info(f"📦 Capabilities for {platform}: {capabilities}")
#
#         if platform.lower() == "android":
#             options = UiAutomator2Options()
#         elif platform.lower() == "ios":
#             options = XCUITestOptions()
#         else:
#             raise ValueError(f"❌ Unsupported platform: {platform}")
#
#         options.load_capabilities(capabilities)
#
#         driver = webdriver.Remote(
#             command_executor=server_url,
#             options=options
#         )
#
#         logging.info("✅ WebDriver started successfully!")
#         return driver
#
#     except WebDriverException as e:
#         logging.error(f"❌ WebDriverException: Unable to connect to Appium server at {server_url}")
#         logging.error(f"🔍 Details: {e}")
#         raise
#
#     except Exception as e:
#         logging.error(f"❌ Unexpected error during driver initialization: {e}", exc_info=True)
#         raise
