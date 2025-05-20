import os
import time
import logging
import pytest
import allure
from utils.driver_manager import get_driver
from utils.appium_server import start_appium_server, stop_appium_server
from utils.allure_steps import attach_screenshot

logger = logging.getLogger("mobile_framework_logger")

# ✅ Add CLI option for platform
def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Target platform to run tests on (android or ios)"
    )

@pytest.fixture
def platform(request):
    platform = request.config.getoption("--platform")
    logger.info(f"🔍 Selected platform: {platform}")
    return platform

# ✅ Start/stop local Appium server (only if needed)
@pytest.fixture(scope="session", autouse=True)
def appium_server():
    if os.getenv("APPIUM_SERVER_URL", "").startswith("http://127.0.0.1"):
        logger.info("🚀 Starting local Appium server for this session...")
        start_appium_server()
        yield
        logger.info("🛑 Stopping Appium server...")
        stop_appium_server()
    else:
        yield

# ✅ Appium driver fixture (single-device)
@pytest.fixture(scope="function")
def driver(request, platform):
    logger.info(f"🚗 Initializing driver for platform: {platform}")
    driver = None
    try:
        driver = get_driver(platform)
        request.cls.driver = driver
        request.cls.platform = platform
        yield driver
    except Exception as e:
        logger.error(f"❌ Failed to start driver: {e}", exc_info=True)
        raise
    finally:
        if driver:
            logger.info("🛑 Quitting driver after test...")
            driver.quit()
        else:
            logger.warning("⚠️ No driver instance found.")

# ✅ Multi-device driver fixture (iOS + Android)
@pytest.fixture(scope="function")
def multidevice_drivers():
    logger.info("🚗 Starting multi-device drivers (User A - iOS, User B - Android)")
    driver_ios = get_driver("ios", instance_name="user_a")
    driver_android = get_driver("android", instance_name="user_b")
    yield driver_ios, driver_android
    logger.info("🛑 Quitting both drivers after multi-device test")
    driver_ios.quit()
    driver_android.quit()

# ✅ Automatically attach screenshot on test failure (for class-based tests)
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        driver = None

        # Try getting driver from class (e.g., self.driver_android / self.driver_ios)
        if hasattr(item, "instance"):
            driver = getattr(item.instance, "driver_android", None) or getattr(item.instance, "driver_ios", None)

        # If function-style test (rare in your case), fallback
        if not driver:
            driver = item.funcargs.get("driver")

        if driver:
            attach_screenshot(driver, name="Auto_Failure_Screenshot", folder="failures")
        else:
            allure.attach("❌ No driver found for screenshot", name="Screenshot Skipped", attachment_type=allure.attachment_type.TEXT)

# ✅ Auto-title and description in Allure reports
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    title = item.name if hasattr(item, "name") else item.nodeid
    allure.dynamic.title(title)
    allure.dynamic.description(f"Test function: {title}")
