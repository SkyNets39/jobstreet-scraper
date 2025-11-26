# crawler.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
import selenium.common.exceptions as SE

import config
from anti_ban import human_delay, small_random_scroll
from parser import extract_links_from_list_page, parse_job_detail


# ---------------------------------------------------------
#  PAGINATION: COLLECT ALL LINKS ACROSS MULTIPLE PAGES
# ---------------------------------------------------------
def collect_all_links(driver: WebDriver):
    all_links = []

    for page in range(1, config.MAX_PAGES_PER_RUN + 1):

        print(f"\n--- Collecting page {page} ---")

        small_random_scroll(driver)
        human_delay()

        links = extract_links_from_list_page(driver, config.BASE_URL)
        print(f"Found {len(links)} links on page {page}.")
        all_links.extend(links)

        if page >= config.MAX_PAGES_PER_RUN:
            print("Reached max pages limit.")
            break

        # Try find NEXT button
        try:
            next_btn = driver.find_element(By.XPATH, '//a[@rel="nofollow next"]')
        except NoSuchElementException:
            print("Next button not found → stopping pagination.")
            break

        print("Clicking NEXT PAGE...")
        driver.execute_script("arguments[0].click();", next_btn)
        human_delay()

    return all_links


# ---------------------------------------------------------
#  SAFE NAVIGATION (handles UC crash)
# ---------------------------------------------------------
def safe_get(driver: WebDriver, url: str):
    """
    UC sometimes drops session or crashes renderer.
    This function safely retries driver.get().
    """
    try:
        driver.get(url)
        return driver
    except Exception as e:
        print("Navigation error → restarting driver...")
        from browser import create_driver
        driver.quit()

        driver = create_driver()
        driver.get(url)
        return driver


# ---------------------------------------------------------
#  MAIN SCRAPER FUNCTION
# ---------------------------------------------------------
def scrape_classification(route=None):
    from browser import create_driver  # avoid circular import

    driver = create_driver()

    CLASS_URL = config.BASE_URL + (route or config.CLASSIFICATION_ROUTE)
    print("Visiting:", CLASS_URL)

    driver.get(CLASS_URL)
    human_delay()

    # STEP 1 — Collect ALL links
    links = collect_all_links(driver)
    print("\nTotal collected links:", len(links))

    job_names = []
    company_names = []
    work_types = []
    salary_ranges = []
    link_list = []

    for idx, link in enumerate(links, start=1):
        print(f"\n[{idx}] Visiting {link}")

        # Safe navigation
        driver = safe_get(driver, link)
        human_delay()

        parsed = parse_job_detail(driver)

        # append into each array
        job_names.append(parsed.get("job_name"))
        company_names.append(parsed.get("company_name"))
        work_types.append(parsed.get("work_type"))
        salary_ranges.append(parsed.get("salary_range"))
        link_list.append(link)

        print(f"[{idx}] Scraped: {parsed}")

        # restart UC every 50 links
        if idx % 50 == 0:
            print("Restarting driver to avoid UC crash...")
            driver.quit()
            driver = create_driver()

    driver.quit()

    # Return dictionary of arrays
    return {
        "Job Name": job_names,
        "Company": company_names,
        "Work Type": work_types,
        "Salary Range": salary_ranges,
        "Link": link_list,
    }
