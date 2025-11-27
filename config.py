# config.py
from typing import List

# --- Defaults (user can override from GUI) ---
COUNTRY_CODE = "id"
JOB_CLASSIFICATION = "jobs-in-information-communication-technology"

# NOTE:
# BASE_URL, CLASSIFICATION_ROUTE, FULL_CLASSIFICATION_ROUTE
# will be dynamically overridden by the GUI and crawler
BASE_URL = f"https://{COUNTRY_CODE}.jobstreet.com"
CLASSIFICATION_ROUTE = f"/{JOB_CLASSIFICATION}"
FULL_CLASSIFICATION_ROUTE = f"{BASE_URL}{CLASSIFICATION_ROUTE}"

# Scraper behavior
MAX_PAGES_PER_RUN = 2  # safe default for testing; GUI will override
HEADLESS = False
WINDOW_SIZE = (1366, 768)

# Delays (anti-ban)
DELAY_MIN = 1.2
DELAY_MAX = 2.4
SCROLL_PAUSE = 0.4

# Retry & timeout
REQUEST_TIMEOUT = 10
RETRY_LIMIT = 3
RETRY_BACKOFF = 2

# Storage
OUTPUT_JSON = "results.json"
OUTPUT_CSV = "results.csv"
COOKIES_FILE = "cookies.pkl"

USER_AGENTS = [
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
   "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

PROXIES: List[str] = [
    # "username:password@1.2.3.4:8000",
]

# Login
ENABLE_LOGIN = False
LOGIN_EMAIL = "your@email.com"
LOGIN_PASSWORD = "yourpassword"
