import os

from collector_core.fingerprint import get_machine_fingerprint

API_REFRESH_INTERVAL_MS = os.environ.get("API_REFRESH_INTERVAL_MS", 1000)
FINGERPRINT = get_machine_fingerprint()
