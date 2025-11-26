import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import config
import random

def create_driver():
    # Mulai dengan options default UC (lebih aman)
    options = uc.ChromeOptions()

    # User agent random (UC support)
    ua = random.choice(config.USER_AGENTS)
    options.add_argument(f"--user-agent={ua}")

    # headless? gunakan format UC
    if config.HEADLESS:
        options.add_argument("--headless=new")

    # Window size
    w, h = config.WINDOW_SIZE
    options.add_argument(f"--window-size={w},{h}")

    # UC tidak butuh flags automation disabled (sudah otomatis diterapkan)
    # Jadi jangan pakai excludeSwitches atau useAutomationExtension

    # Optional: mengurangi fingerprinting
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")

    # Buat driver dengan UC (tanpa experimental_options lama)
    driver = uc.Chrome(options=options)

    return driver
