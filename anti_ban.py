# anti_ban.py
import random
import time
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import config


def human_delay():
    """Sleep random amount in configured range."""
    t = random.uniform(config.DELAY_MIN, config.DELAY_MAX)
    time.sleep(t)


def small_random_scroll(driver: WebDriver):
    """Do small incremental scrolls to simulate reading."""
    height = driver.execute_script("return document.body.scrollHeight || document.documentElement.scrollHeight;")
    # do 2-5 small scrolls
    steps = random.randint(2, 5)
    for i in range(steps):
        fraction = (i + 1) / steps
        y = int(height * fraction * random.uniform(0.2, 0.95))
        driver.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(config.SCROLL_PAUSE * random.uniform(0.8, 1.4))


def jitter_mouse(driver: WebDriver, times: int = 3):
    """Move mouse to random points on the page slightly (best-effort)."""
    try:
        actions = ActionChains(driver)
        w = driver.execute_script("return window.innerWidth")
        h = driver.execute_script("return window.innerHeight")
        for _ in range(times):
            x = random.randint(int(w * 0.1), int(w * 0.9))
            y = random.randint(int(h * 0.1), int(h * 0.9))
            actions.move_by_offset(x, y).perform()
            time.sleep(random.uniform(0.2, 0.6))
            # reset origin for next move
            actions.reset_actions()
    except Exception:
        # some drivers may not support move_by_offset consistently; ignore
        pass


def detect_captcha_or_block(driver: WebDriver) -> bool:
    """Return True if a captcha or block page is likely present."""
    # Common heuristics
    page_source = driver.page_source.lower()
    if "captcha" in page_source or "cloudflare" in page_source or "access denied" in page_source:
        return True
    # check for known recaptcha iframe or elements
    try:
        frames = driver.find_elements(By.TAG_NAME, "iframe")
        for f in frames:
            src = f.get_attribute("src") or ""
            if "recaptcha" in src or "captcha" in src:
                return True
    except Exception:
        pass
    return False


def apply_pre_visit_behaviors(driver: WebDriver):
    """Actions to do before visiting a page or starting to parse."""
    small_random_scroll(driver)
    jitter_mouse(driver)
    human_delay()
