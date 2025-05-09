import os
import logging
import json
from dotenv import load_dotenv

# --------------------------------------------
# ✅ Setup Logging
# --------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --------------------------------------------
# ✅ Resolve base directory safely
# --------------------------------------------
base_dir = os.getcwd()

# --------------------------------------------
# ✅ Load .env File
# --------------------------------------------
dotenv_path = os.path.join(base_dir, ".env")
env = os.getenv("ENV", "qa")  # Default to qa if not set

if os.path.exists(dotenv_path):
    logging.info(f"🔍 Loading .env from: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    logging.warning(f"⚠️ No .env file found at {dotenv_path}")

# --------------------------------------------
# ✅ Load env-specific JSON Config (e.g., qa.json)
# --------------------------------------------
config_file = os.path.join(base_dir, "config", f"{env}.json")
if not os.path.exists(config_file):
    logging.error(f"❌ Config file not found: {config_file}")
    raise FileNotFoundError(f"Missing config file: {config_file}")

with open(config_file, "r") as f:
    ENV_CONFIG = json.load(f)

logging.info(f"✅ Loaded config: {config_file}")

# --------------------------------------------
# ✅ Helper to get config value
# --------------------------------------------
def get_config_value(key: str, default: str = ""):
    return os.getenv(key) or ENV_CONFIG.get(key) or default

# --------------------------------------------
# ✅ Final CONFIG Dictionary (with dynamic BStack support)
# --------------------------------------------

is_browserstack = "browserstack" in get_config_value("APPIUM_SERVER_URL").lower()

CONFIG = {
    "android": {
        "platformName": "Android",
        "appium:app": get_config_value("ANDROID_APP_PATH"),
        "appium:deviceName": get_config_value("ANDROID_DEVICE", "Samsung Galaxy S22"),
        "appium:udid": get_config_value("ANDROID_UDID"),
        "appium:platformVersion": get_config_value("ANDROID_VERSION", "12"),
        "appium:automationName": "UiAutomator2",
        "project": "Genius Meter App",
        "build": "Regression Build 1",
        "name": "Android Test",
        "server_url": get_config_value("APPIUM_SERVER_URL")
    },
    "ios": {
        "platformName": "iOS",
        "appium:app": get_config_value("IOS_APP_PATH"),
        "appium:deviceName": get_config_value("IOS_DEVICE", "iPhone 14 Pro"),
        "appium:platformVersion": get_config_value("IOS_VERSION", "16"),
        "appium:automationName": "XCUITest",
        "appium:useNewWDA": True,
        "appium:autoAcceptAlerts": True,
        "appium:autoDismissAlerts": True,
        "appium:wdaLocalPort": 8100,
        "appium:wdaStartupRetries": 2,
        "appium:wdaLaunchTimeout": 60000,
        "server_url": get_config_value("APPIUM_SERVER_URL")
    },

}

# ✅ Conditionally add bstack:options only if using BrowserStack
if is_browserstack:
    CONFIG["android"]["bstack:options"] = {
        "userName": get_config_value("BROWSERSTACK_USERNAME"),
        "accessKey": get_config_value("BROWSERSTACK_ACCESS_KEY")
    }
    CONFIG["ios"]["bstack:options"] = {
        "userName": get_config_value("BROWSERSTACK_USERNAME"),
        "accessKey": get_config_value("BROWSERSTACK_ACCESS_KEY")
    }

# ✅ Debug logs
logging.info("✅ Final CONFIG loaded successfully!")
logging.info(f"📱 ANDROID Config: {CONFIG.get('android')}")
logging.info(f"📱 IOS Config: {CONFIG.get('ios')}")
logging.info(f"📦 Android App Path: {get_config_value('ANDROID_APP_PATH')}")
logging.info(f"📦 iOS App Path: {get_config_value('IOS_APP_PATH')}")
logging.info(f"📡 Appium Server URL: {get_config_value('APPIUM_SERVER_URL')}")
