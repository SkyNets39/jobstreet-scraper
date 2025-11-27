# Jobstreet Scraper — Automated Job Data Extraction (Python + Selenium + UC)

A fully automated and anti-ban web scraper built for extracting job listings by category from **Jobstreet** using:

- **Python + Selenium**
- **Undetected-Chromedriver (UC)**
- **Human-like anti-bot behaviors**
- **Tkinter Desktop GUI**
- **Multithreaded scraping worker**
- **Pagination handling**
- **Crash-safe browser recovery**
- **CSV output via pandas**

This project scrapes job listings (titles, companies, work types, salary ranges, and detail URLs) from **Jobstreet across any country**, using a **flexible classification URL builder** and a **safe multithreaded scraper engine**.

---

## 🚀 Features

### ✅ Desktop GUI (Tkinter)
A simple and user-friendly interface with:

- Country code selection (id/my/sg/ph)
- Job classification route input
- Maximum pages setting
- CSV output path selection
- Real-time logging panel
- Start & Stop controls
- Background scraping worker (UI stays responsive)

---

### ✅ Anti-Ban & Human Behavior Simulation
- Randomized human-like delays  
- Smooth incremental scrolling  
- Random mouse jitter movements  
- User-Agent rotation  
- Undetected-Chromedriver stealth mode  
- CAPTCHA/block page heuristic detection  
- Natural pagination clicking  
- No multi-threaded or parallel requests  

---

### ✅ Stable Long-Run Scraping
- Safe wrapper around `driver.get()`  
- Automatic browser restart every 50 jobs  
- Auto recovery if UC crashes  
- Threading-based stop mechanism  
- Saves all collected data even when stopped early  

---

### ✅ Flexible URL Classification
Using `build_classification_url(country, classification)`:

Works with:
- id.jobstreet.com  
- my.jobstreet.com  
- sg.jobstreet.com  
- ph.jobstreet.com  

…and supports any `jobs-in-xxxx` classification page.

---

### ✅ Clean CSV Output
Columns:
- Job Name  
- Company  
- Work Type  
- Salary Range  
- Link  

Saved using UTF-8-SIG (Excel-friendly).

---

## 🛠 Tech Stack

| Component | Technology |
|----------|------------|
| UI | Tkinter |
| Automation | Selenium WebDriver |
| Stealth | undetected-chromedriver |
| Parsing | Selenium + XPath |
| Exporting | pandas |
| Language | Python 3.11 |
| OS | Windows 10/11 (tested) |

---

## 📦 Requirements

### 🔧 **Prerequisites**
Install:

- **Python 3.11.x** (UC is unstable on Python 3.12+ → use 3.11 for best compatibility)
- Chromedriver (latest version)
- Git (optional)

Install Dependencies:
```bash
pip install selenium undetected-chromedriver pandas
```

---

## ⚙️ Configuration Overview
All defaults live in config.py, but are dynamically overridden by the GUI.
- Key config values:
- COUNTRY_CODE
- JOB_CLASSIFICATION
- MAX_PAGES_PER_RUN
- HEADLESS
- USER_AGENTS
- DELAY_MIN, DELAY_MAX

## ▶️ Running the Scraper
### GUI Mode
```python
python app_gui.py
```
#### GUI Input and Operation
1. Seek the job classification you want to scrape
<img width="1912" height="1138" alt="image" src="https://github.com/user-attachments/assets/70116ead-6996-4fe4-9223-eb7bc87d2346" />

2. Copy the job classification path URL and paste it to GUI. Make sure to input the correct country code.
<img width="2880" height="1710" alt="image" src="https://github.com/user-attachments/assets/e45e7903-4a80-4b01-a42d-fb0a817f5576" />

3. Lastly you can click "Start" button to start the scrap and "Stop" to stop the scraping process

### CLI Mode
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
app_gui.py | GUI, threading, logging, run/stop control
utils.py | URL builder for any country + classification

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
