from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def extract_links_from_list_page(driver: WebDriver, base_url: str):
    jobcards = driver.find_elements(By.XPATH, '//article[@data-card-type="JobCard"]')

    links = []
    for jobcard in jobcards:
        try:
            link_elem = jobcard.find_element(By.XPATH, './/a[@data-automation="job-list-item-link-overlay"]')
            href = link_elem.get_attribute("href")
            full_link = base_url + href if href.startswith("/") else href
            links.append(full_link)
        except:
            continue

    return links


def parse_job_detail(driver: WebDriver):
    try:
        job_name = driver.find_element(By.XPATH, '//h1').text.strip()
    except:
        job_name = None

    try:
        company_name = driver.find_element(By.XPATH, '//span[@data-automation="advertiser-name"]').text.strip()
    except:
        company_name = None

    try:
        work_type = driver.find_element(By.XPATH, '//span[@data-automation="job-detail-work-type"]').text.strip()
    except:
        work_type = None

    try:
        salary_range = driver.find_element(By.XPATH, '//span[@data-automation="job-detail-salary"]').text.strip()
    except:
        salary_range = None

    return {
        "job_name": job_name,
        "company_name": company_name,
        "work_type": work_type,
        "salary_range": salary_range,
    }
