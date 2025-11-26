from typing import List

# --- Basic settings ---
BASE_URL = "https://id.jobstreet.com"
CLASSIFICATION_ROUTE = "/id/jobs-in-information-communication-technology"
RESULTS_PER_PAGE = 20  # approximate, not strictly required by scraper
MAX_PAGES_PER_RUN = 2  # adjust to your acceptable daily limit
HEADLESS = False  # recommended False to reduce detection
WINDOW_SIZE = (1366, 768)

# Delays (for anti-ban)
DELAY_MIN = 1.2
DELAY_MAX = 2.4
SCROLL_PAUSE = 0.4

# --- Retry & timeout ---
REQUEST_TIMEOUT = 10  # seconds for explicit waits
RETRY_LIMIT = 3
RETRY_BACKOFF = 2  # multiplier for exponential backoff

# --- Storage ---
OUTPUT_JSON = "results.json"
OUTPUT_CSV = "results.csv"
COOKIES_FILE = "cookies.pkl"

USER_AGENTS = [
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
   "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# --- Optional proxies list: format "ip:port" or "user:pass@ip:port" if needed ---
PROXIES: List[str] = [
    # "username:password@1.2.3.4:8000",
    # "5.6.7.8:3128",
]

# --- Login ---
ENABLE_LOGIN = False
LOGIN_EMAIL = "your@email.com"
LOGIN_PASSWORD = "yourpassword"