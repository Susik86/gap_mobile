import pytest
import logging
from utils.appium_server import start_appium_server, stop_appium_server
from utils.driver_manager import get_driver

def pytest_addoption(parser):
    """Add CLI options for pytest."""
    parser.addoption("--platform", action="store", default="android", help="Platform to run tests on")

@pytest.fixture
def platform(request):
    """Retrieve platform from pytest CLI options."""
    platform = request.config.getoption("--platform")
    logger = logging.getLogger("mobile_framework_logger")
    logger.info(f"🔍 Selected platform: {platform}")  # ✅ Debugging log
    return platform

# ✅ Start Appium only ONCE per session (before tests start)
@pytest.fixture(scope="session", autouse=True)
def appium_server():
    """Start Appium server before the test session and keep it running."""
    logger = logging.getLogger("mobile_framework_logger")
    logger.info("🚀 Starting Appium server before tests...")

    start_appium_server()  # ✅ Start Appium only once
    yield  # ✅ Tests will run now (Appium stays active)

    logger.info("🛑 Stopping Appium server AFTER all tests...")
    stop_appium_server()

# ✅ WebDriver is reset **for each test case** (NOT class)
@pytest.fixture(scope="function")
def driver(request):
    """Initialize Appium WebDriver for each test case (not class)."""
    logger = logging.getLogger("mobile_framework_logger")
    platform = request.config.getoption("--platform")

    if not platform:
        logger.error("❌ Missing '--platform' argument! Use --platform=android or --platform=ios")
        raise pytest.UsageError("❌ Missing '--platform' argument! Use --platform=android or --platform=ios")

    logger.info(f"🚗 Starting WebDriver for {platform}...")

    driver = None
    try:
        driver = get_driver(platform)
        request.cls.driver = driver  # ✅ Attach driver to test instance
        request.cls.platform = platform  # ✅ Store platform separately
        yield driver  # ✅ Yield the driver (test will run)

    except Exception as e:
        logger.error(f"❌ WebDriver initialization failed: {str(e)}", exc_info=True)
        raise

    finally:
        if driver:
            logger.info("🛑 Quitting WebDriver after test case...")
            driver.quit()
            logger.info("✅ WebDriver stopped successfully.")
        else:
            logger.warning("⚠️ WebDriver was not initialized, skipping quit.")
