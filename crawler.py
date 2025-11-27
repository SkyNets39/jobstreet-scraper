# crawler.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

import config
from anti_ban import human_delay, small_random_scroll
from parser import extract_links_from_list_page, parse_job_detail
from browser import create_driver
from utils import build_classification_url


def collect_all_links(driver: WebDriver, base_url: str, max_pages: int):
    all_links = []

    for page in range(1, max_pages + 1):
        print(f"\n--- Collecting page {page} ---")

        small_random_scroll(driver)
        human_delay()

        links = extract_links_from_list_page(driver, base_url)
        print(f"Found {len(links)} links on page {page}.")
        all_links.extend(links)

        if page >= max_pages:
            print("Reached max pages limit.")
            break

        # Find NEXT PAGE button
        try:
            next_btn = driver.find_element(By.XPATH, '//a[@rel="nofollow next"]')
        except NoSuchElementException:
            try:
                next_btn = driver.find_element(By.XPATH, '//a[@title="Selanjutnya"]')
            except NoSuchElementException:
                print("Next button not found → stopping pagination.")
                break

        print("Clicking NEXT PAGE...")
        driver.execute_script("arguments[0].click();", next_btn)
        human_delay()

    return all_links


def safe_get(driver: WebDriver, url: str):
    """Retry loading URL once if UC crashes"""
    try:
        driver.get(url)
        return driver
    except Exception as e:
        print("Navigation error → restarting driver...", e)
        driver.quit()
        driver = create_driver()
        driver.get(url)
        return driver


def scrape_classification(country: str = None, classification: str = None):
    """
    Main function: country + classification → URL → scraping
    """

    # Build final URL
    country = country or config.COUNTRY_CODE
    classification = classification or config.JOB_CLASSIFICATION

    base_url, route, full_url = build_classification_url(country, classification)

    # Update config
    config.COUNTRY_CODE = country
    config.BASE_URL = base_url
    config.CLASSIFICATION_ROUTE = route
    config.FULL_CLASSIFICATION_ROUTE = full_url

    print("Visiting:", full_url)

    driver = create_driver()
    driver.get(full_url)
    human_delay()

    # STEP 1: collect all links
    links = collect_all_links(driver, base_url, config.MAX_PAGES_PER_RUN)
    print("\nTotal collected links:", len(links))

    job_names = []
    company_names = []
    work_types = []
    salary_ranges = []
    link_list = []

    # STEP 2: visit each job
    for idx, link in enumerate(links, start=1):
        print(f"\n[{idx}] Visiting {link}")

        driver = safe_get(driver, link)
        human_delay()

        parsed = parse_job_detail(driver)

        job_names.append(parsed.get("job_name"))
        company_names.append(parsed.get("company_name"))
        work_types.append(parsed.get("work_type"))
        salary_ranges.append(parsed.get("salary_range"))
        link_list.append(link)

        print(f"[{idx}] Scraped:", parsed)

        if idx % 50 == 0:
            print("Restarting driver (stability)...")
            driver.quit()
            driver = create_driver()

    driver.quit()

    return {
        "Job Name": job_names,
        "Company": company_names,
        "Work Type": work_types,
        "Salary Range": salary_ranges,
        "Link": link_list,
    }
