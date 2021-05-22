import os

HTTP_RETRIES = os.getenv("HTTP_RETRIES", 3)
HTTP_BACKOFF_FACTOR = float(os.getenv("HTTP_BACKOFF_FACTOR", 0.1))
HTTP_STATUS_FORCELIST = os.getenv("HTTP_RETRIES", None)
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", 30))
