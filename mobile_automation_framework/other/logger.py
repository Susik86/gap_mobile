import logging
import os
from datetime import datetime

# ✅ Ensure Log Directory Exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Ensures the directory exists

# ✅ Define Log File (Rotates Daily)
log_filename = os.path.join(LOG_DIR, f"test_log_{datetime.now().strftime('%Y-%m-%d')}.log")

# ✅ Configure Logging (Ensure No Duplicate Handlers)
logger = logging.getLogger("mobile_framework_logger")
if not logger.handlers:  # Prevent duplicate handlers if this module is imported multiple times
    logger.setLevel(logging.INFO)

    # ✅ File Handler (Logs to File)
    file_handler = logging.FileHandler(log_filename, mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"))
    file_handler.setLevel(logging.INFO)

    # ✅ Stream Handler (Logs to Console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    stream_handler.setLevel(logging.INFO)

    # ✅ Add Handlers (Only Once)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

logger.info("✅ Logger initialized successfully!")
