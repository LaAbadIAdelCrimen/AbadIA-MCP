import os

# Base paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE_PATH = os.path.join(PROJECT_ROOT, "storage")

# Ensure storage directory exists
if not os.path.exists(STORE_PATH):
    os.makedirs(STORE_PATH)

# Common configuration
ABADIA_SERVER_URL = os.getenv("ABADIA_SERVER_URL")
