import os
import time
import allure
from allure_commons.types import AttachmentType


def attach_screenshot(driver, name="Screenshot", folder=""):
    """
    Takes a screenshot using the driver and attaches it to the Allure report.
    Automatically adds platform name (android/ios) as part of the folder path.
    """

    timestamp = str(int(time.time()))

    # ✅ Detect platform from driver capabilities
    try:
        caps = driver.capabilities
        platform = caps.get("platformName") or caps.get("appium:platformName") or "unknown"
        platform = platform.lower()
    except Exception:
        platform = "unknown"

    # ✅ Build screenshot folder path
    base_dir = os.path.join(os.getcwd(), "results", "screenshots", platform)
    if folder:
        screenshot_dir = os.path.join(base_dir, folder)
    else:
        screenshot_dir = base_dir

    os.makedirs(screenshot_dir, exist_ok=True)

    # ✅ Save screenshot with timestamp
    screenshot_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
    driver.save_screenshot(screenshot_path)

    # ✅ Attach to Allure report
    allure.attach.file(screenshot_path, name=name, attachment_type=AttachmentType.PNG)


def attach_text(name, content):
    """
    Attaches a text block to the Allure report.
    """
    allure.attach(content, name=name, attachment_type=AttachmentType.TEXT)


def attach_log(name, filepath):
    """
    Attaches a log file to the Allure report.
    """
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        allure.attach(content, name=name, attachment_type=AttachmentType.TEXT)


def step(description):
    """
    Decorator for wrapping a test step with description in the Allure report.
    Usage:
        @step("Tap login button")
        def tap_login():
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with allure.step(description):
                return func(*args, **kwargs)
        return wrapper
    return decorator
