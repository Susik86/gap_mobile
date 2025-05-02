import pytest
import logging
import os
import allure
import time
from utils.driver_manager import get_driver
from utils.appium_server import start_appium_server, stop_appium_server

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

# ✅ Start/stop local Appium server only if needed
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

# ✅ Appium driver per test
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

# ✅ Auto-attach screenshot on test failure
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        driver = getattr(item._request.cls, "driver", None)
        if driver:
            screenshot_dir = os.path.join(os.getcwd(), "results", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            file_name = f"{item.name}_{int(time.time())}.png"
            file_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(file_path)
            allure.attach.file(file_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

# ✅ Auto title/description for Allure
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    allure.dynamic.title(item.name)
    allure.dynamic.description(f"Test function: {item.name}")
