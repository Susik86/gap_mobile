import time
import logging
import requests
from appium.webdriver.appium_service import AppiumService

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Create an Appium service instance
appium_service = AppiumService()

# Possible Appium URLs
APPIUM_URLS = [
    "http://127.0.0.1:4723/wd/hub/status"
]

def is_appium_running():
    """Check if Appium server is already running on any available URL."""
    for url in APPIUM_URLS:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logging.info(f"✅ Appium is running at {url}")
                return True
        except requests.exceptions.RequestException:
            continue
    return False

def start_appium_server():
    """Start the Appium server using AppiumService."""
    if is_appium_running():
        logging.info("✅ Appium is already running.")
        return  # Don't start it again if already running

    logging.info("🚀 Starting Appium server...")
    appium_service.start(args=["--port", "4723", "--base-path", "/wd/hub"])

    # Wait and check if it's actually running
    for _ in range(10):
        if is_appium_running():
            logging.info("✅ Appium server started successfully.")
            return
        time.sleep(1)

    logging.error("❌ Failed to start Appium server!")
    raise RuntimeError("Appium server did not start successfully.")

def stop_appium_server():
    """Stop the Appium server safely."""
    if appium_service.is_running:
        logging.info("🛑 Stopping Appium server...")
        appium_service.stop()
        logging.info("✅ Appium server stopped.")
    else:
        logging.info("ℹ️ Appium server is not running, nothing to stop.")

# Example usage:
if __name__ == "__main__":
    start_appium_server()
    time.sleep(5)  # Simulating some Appium activity
    stop_appium_server()
