import os
import logging
import json
from dotenv import load_dotenv

# --------------------------------------------
# ✅ Setup Logging (Before any logging statements)
# --------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --------------------------------------------
# ✅ Load Environment Variables (.env file)
# --------------------------------------------
env = os.getenv("ENV", "qa")  # Default to "qa"
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "utils", ".env")

if os.path.exists(dotenv_path):
    logging.info(f"🔍 Loading .env from: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    logging.warning(f"⚠️ No .env file found at {dotenv_path}. Environment variables may not be loaded.")

# ✅ Debugging: Print loaded environment variables
logging.info(f"🔍 Current Environment: {env}")
logging.info(f"🔍 ANDROID_APP_PATH: {os.getenv('ANDROID_APP_PATH')}")
logging.info(f"🔍 IOS_APP_PATH: {os.getenv('IOS_APP_PATH')}")

# --------------------------------------------
# ✅ Load Environment-Specific JSON Config
# --------------------------------------------
config_file = os.path.join(os.path.dirname(__file__), f"{env}.json")  # ✅ Fix path

if not os.path.exists(config_file):
    logging.error(f"❌ Config file not found: {config_file}. Please check the environment setup.")
    raise FileNotFoundError(f"Missing config file: {config_file}")

with open(config_file, "r") as f:
    ENV_CONFIG = json.load(f)

logging.info(f"✅ Successfully loaded configuration from {config_file}")

# --------------------------------------------
# ✅ Final Appium CONFIG Dictionary
# --------------------------------------------
CONFIG = {
    "android": {
        "platformName": "Android",
        "appium:app": os.getenv("ANDROID_APP_PATH"),  # ✅ Use os.getenv()
        "appium:deviceName": os.getenv("ANDROID_DEVICE", "Unknown Device"),
        "appium:platformVersion": os.getenv("ANDROID_VERSION", "Unknown Version"),
        "appium:udid": os.getenv("ANDROID_UDID", ""),  # ✅ Fix for real devices
        "appium:automationName": "UiAutomator2",
        "appium:autoGrantPermissions": True,
    },
    "ios": {
        "platformName": "iOS",
        "appium:app": os.getenv("IOS_APP_PATH"),
        "appium:deviceName": os.getenv("IOS_DEVICE", "iPhone 14 Pro"),
        "appium:platformVersion": os.getenv("IOS_VERSION", "16.4"),
        "appium:udid": os.getenv("IOS_UDID", None),
        "appium:automationName": "XCUITest",
        "appium:useNewWDA": True,  # ✅ Ensure WDA restarts properly
        "appium:wdaLaunchTimeout": 60000,  # ✅ Waits for WDA startup
        "appium:wdaStartupRetries": 2,  # ✅ Retries if WDA fails
        "appium:wdaLocalPort": 8100,  # ✅ Ensures WDA runs on port 8100
        "appium:autoAcceptAlerts": True,  # ✅ Prevents automatic "Save Password"
    }
}


# ✅ Debugging Output
logging.info(f"✅ CONFIG Loaded Successfully!")
logging.info(f"🔍 Selected capabilities for Android: {CONFIG.get('android')}")
logging.info(f"🔍 Selected capabilities for iOS: {CONFIG.get('ios')}")
