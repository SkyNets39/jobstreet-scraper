# Jobstreet Scraper — Automated Job Data Extraction (Python + Selenium + UC)

A fully automated and anti-ban web scraper built for extracting job listings by category from **Jobstreet** using:

- **Selenium WebDriver**
- **Undetected-Chromedriver (UC)**
- **Human-like anti-bot behavior**
- **Modular architecture**
- **Pagination support**
- **Crash-safe session recovery**
- **Export to JSON or CSV using pandas**

This scraper collects job titles, company names, work types, salary ranges, and detail page URLs across multiple pages — safely bypassing common bot detection triggers.

---

## 🚀 Features

### ✅ **Anti-ban & Human Behavior Simulation**
- Random human-like delays  
- Small incremental scrolling  
- Mouse jitter simulation  
- Random user-agent rotation  
- UC stealth mode (bypasses WebDriver detection)

### ✅ **Stable Long-Run Scraping**
- Safe navigation wrapper to recover from UC crashes
- Automatic Chrome restart every 50 jobs
- Graceful retry when encountering dead tabs or session drops

### ✅ **Real Pagination**
- Automatically scrapes multiple pages using the “Next” button
- Configurable maximum pages (default `5`)

### ✅ **Modular Design**
Each responsibility separated cleanly:
- browser.py → Chrome driver & UC setup
- crawler.py → Pagination + scraping workflow
- parser.py → HTML parsing for list pages & detail pages
- anti_ban.py → Human-like actions & bot avoidance
- config.py → Centralized configurations
- main.py → Runner & CSV exporter


### ✅ **Clean Output**
- Saves results into `results.csv`
- Columns:
  - Job Name  
  - Company  
  - Work Type  
  - Salary Range  
  - Link  

---

## 🛠 Tech Stack

| Component | Technology |
|----------|------------|
| Language | Python 3.11 (recommended) |
| Automation | Selenium WebDriver |
| Stealth | undetected-chromedriver |
| Parsing | Selenium + XPath |
| Exporting | pandas DataFrame → CSV |
| OS | Windows 10/11 (tested) |

---

## 📦 Requirements

### 🔧 **Prerequisites**
Install:

- **Python 3.11.x** (UC is unstable on Python 3.12+ → use 3.11 for best compatibility)
- Chromedriver (latest version)
- Git (optional)

Install Library:
```bash
pip install selenium undetected-chromedriver pandas
```

---

## ⚙️ Important Configuration
Edit all settings in config.py:
- BASE_URL = "https://id.jobstreet.com" (You can change the country of Jobstreet by changing the "id" which default to Indonesia)
- CLASSIFICATION_ROUTE = "/id/jobs-in-accounting" (Choose the route for job classification)
- USER_AGENTS (You can choose any user agents)

## ▶️ Running the Scraper
```python
python main.py
```
## Architecture Overview
| File | Description |
|----------|------------|
browser.py | UC driver setup (stealth, UA rotation, window config)
crawler.py | Pagination, link collection, safe navigation
parser.py | Extract job links & job details via XPath
anti_ban.py | Scroll, delay, mouse movement, captcha heuristics
config.py | User configuration for routes, delay, UA, etc
main.py | Runner + CSV export
results.csv | Output CSV file

## 🔒 Anti-Ban Strategies Used
This scraper is engineered to avoid triggering Jobstreet’s bot detection:
- UC hides webdriver fingerprints
- Random User-Agent
- Random scroll behavior
- Mouse movement (simulated jitter)
- Humanized delay patterns
- No parallel requests
- Works in normal Chrome (not headless)
- Pagination is clicked naturally, not forced via URL skip
These strategies mimic human browsing very closely.

## 📬 Contact
If you want to discuss code structure, optimizations, or use this project in interviews, feel free to reach out:
williamwinata37@gmail.com
