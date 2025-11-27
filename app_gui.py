# app_gui.py
import threading
import queue
import time
import os
import traceback
from typing import List
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox

from selenium.webdriver.common.by import By

from browser import create_driver
from parser import extract_links_from_list_page, parse_job_detail
from anti_ban import small_random_scroll, human_delay, detect_captcha_or_block
from utils import build_classification_url

import config


class ScrapeWorker(threading.Thread):
    def __init__(self, base_url: str, route: str, max_pages: int, output_file: str,
                 log_queue: queue.Queue, stop_event: threading.Event):
        super().__init__(daemon=True)
        self.base_url = base_url
        self.route = route
        self.max_pages = max_pages
        self.output_file = output_file
        self.log_queue = log_queue
        self.stop_event = stop_event
        self.driver = None

    def log(self, *args):
        self.log_queue.put(" ".join(str(a) for a in args))

    def safe_quit_driver(self):
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass
        self.driver = None

    def safe_get(self, url: str):
        if self.stop_event.is_set():
            raise RuntimeError("Stop requested")

        try:
            self.driver.get(url)
            return
        except Exception as e:
            self.log("Navigation error:", repr(e), "Restarting browser...")
            self.safe_quit_driver()

            if self.stop_event.is_set():
                raise RuntimeError("Stop requested")

            self.driver = create_driver()
            time.sleep(1)
            self.driver.get(url)

    def collect_links_paginated(self) -> List[str]:
        from parser import extract_links_from_list_page
        links_acc = []

        for page in range(1, self.max_pages + 1):
            if self.stop_event.is_set():
                self.log("Stop detected during pagination.")
                break

            self.log(f"Collecting page {page}...")
            try:
                small_random_scroll(self.driver)
            except:
                pass

            human_delay()

            try:
                links = extract_links_from_list_page(self.driver, self.base_url)
            except Exception as e:
                self.log("Failed to extract links:", e)
                links = []

            self.log(f"Found {len(links)} links.")
            links_acc.extend(links)

            if page >= self.max_pages:
                break

            try:
                try:
                    next_btn = self.driver.find_element(By.XPATH, '//a[@rel="nofollow next"]')
                except:
                    next_btn = self.driver.find_element(By.XPATH, '//a[@title="Selanjutnya"]')

                self.driver.execute_script("arguments[0].click();", next_btn)
                human_delay()
            except Exception:
                self.log("Next button not found — stopping.")
                break

        return links_acc

    def run(self):
        try:
            self.log("Starting driver...")
            self.driver = create_driver()

            full_url = f"{self.base_url}{self.route}"
            self.log("Visiting:", full_url)

            self.safe_get(full_url)
            human_delay()

            links = self.collect_links_paginated()
            self.log(f"Total collected links: {len(links)}")

            # result lists
            job_names = []
            companies = []
            work_types = []
            salaries = []
            link_list = []

            for idx, link in enumerate(links, start=1):
                if self.stop_event.is_set():
                    break

                self.log(f"[{idx}] Visiting {link}")
                self.safe_get(link)
                human_delay()

                try:
                    parsed = parse_job_detail(self.driver)
                except:
                    parsed = {"job_name": None, "company_name": None,
                              "work_type": None, "salary_range": None}

                job_names.append(parsed["job_name"])
                companies.append(parsed["company_name"])
                work_types.append(parsed["work_type"])
                salaries.append(parsed["salary_range"])
                link_list.append(link)

                self.log(f"[{idx}] Scraped: {parsed}")

                if idx % 50 == 0:
                    self.log("Restarting driver...")
                    self.safe_quit_driver()
                    self.driver = create_driver()

            # Save CSV
            df = pd.DataFrame({
                "Job Name": job_names,
                "Company": companies,
                "Work Type": work_types,
                "Salary Range": salaries,
                "Link": link_list,
            })

            os.makedirs(os.path.dirname(self.output_file) or ".", exist_ok=True)
            df.to_csv(self.output_file, index=False, encoding="utf-8-sig")
            self.log(f"Saved {len(df)} rows to {self.output_file}")

        except Exception as e:
            self.log("ERROR:", repr(e))
            self.log(traceback.format_exc())
        finally:
            self.safe_quit_driver()
            self.log("Driver closed. Finished.")


class ScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jobstreet Scraper (Flexible URL)")
        self.root.geometry("850x650")

        self.log_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.worker = None

        self.build_ui()
        self.root.after(200, self.poll_log_queue)

    def build_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="Country Code (ex: id, my, sg, ph)").grid(row=0, column=0, sticky="w")
        self.country_var = tk.StringVar(value=config.COUNTRY_CODE)
        ttk.Entry(frm, textvariable=self.country_var, width=10).grid(row=1, column=0, sticky="w")

        ttk.Label(frm, text="Job Classification").grid(row=0, column=1, sticky="w")
        self.class_var = tk.StringVar(value=config.JOB_CLASSIFICATION)
        ttk.Entry(frm, textvariable=self.class_var, width=50).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Max Pages").grid(row=0, column=2, sticky="w")
        self.pages_var = tk.IntVar(value=config.MAX_PAGES_PER_RUN)
        ttk.Entry(frm, textvariable=self.pages_var, width=6).grid(row=1, column=2, sticky="w")

        ttk.Label(frm, text="Output CSV").grid(row=2, column=0, sticky="w", pady=(10,0))
        self.output_var = tk.StringVar(value=config.OUTPUT_CSV)
        ttk.Entry(frm, textvariable=self.output_var, width=40).grid(row=3, column=0, sticky="w")

        ttk.Button(frm, text="Browse...", command=self.browse_file).grid(row=3, column=1)

        # buttons
        btn_frm = ttk.Frame(self.root, padding=10)
        btn_frm.pack(fill="x")

        ttk.Button(btn_frm, text="Start", command=self.on_start).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frm, text="Stop", command=self.on_stop).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frm, text="Clear Log", command=self.clear_log).grid(row=0, column=2, padx=5)

        # log
        log_frm = ttk.Frame(self.root, padding=10)
        log_frm.pack(fill="both", expand=True)

        self.log_widget = scrolledtext.ScrolledText(log_frm, wrap="word", state="disabled")
        self.log_widget.pack(fill="both", expand=True)

    def browse_file(self):
        f = filedialog.asksaveasfilename(defaultextension=".csv",
                                         filetypes=[("CSV", "*.csv")])
        if f:
            self.output_var.set(f)

    def on_start(self):
        if self.worker and self.worker.is_alive():
            messagebox.showinfo("Info", "Scraper already running.")
            return

        country = self.country_var.get().strip().lower()
        classification = self.class_var.get().strip()

        try:
            base_url, route, full_url = build_classification_url(country, classification)
        except Exception as e:
            messagebox.showerror("Error", e)
            return

        try:
            max_pages = int(self.pages_var.get())
            if max_pages <= 0:
                raise ValueError()
        except:
            messagebox.showerror("Error", "Max Pages must be positive integer.")
            return

        out_file = self.output_var.get().strip()

        # update global config
        config.COUNTRY_CODE = country
        config.JOB_CLASSIFICATION = classification
        config.BASE_URL = base_url
        config.CLASSIFICATION_ROUTE = route
        config.FULL_CLASSIFICATION_ROUTE = full_url
        config.MAX_PAGES_PER_RUN = max_pages
        config.OUTPUT_CSV = out_file

        # clear states
        self.stop_event.clear()
        self.log_queue.queue.clear()

        self.worker = ScrapeWorker(base_url, route, max_pages, out_file,
                                   self.log_queue, self.stop_event)
        self.worker.start()

        self.log(f"Started: {full_url} pages={max_pages} → {out_file}")

    def on_stop(self):
        if not self.worker or not self.worker.is_alive():
            messagebox.showinfo("Info", "No running process.")
            return

        self.stop_event.set()
        self.log("Stop requested...")

    def clear_log(self):
        self.log_widget.config(state="normal")
        self.log_widget.delete("1.0", "end")
        self.log_widget.config(state="disabled")

    def log(self, *args):
        self.log_queue.put(" ".join(str(a) for a in args))

    def poll_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_widget.config(state="normal")
                self.log_widget.insert("end", msg + "\n")
                self.log_widget.see("end")
                self.log_widget.config(state="disabled")
        except queue.Empty:
            pass

        self.root.after(200, self.poll_log_queue)


def main():
    root = tk.Tk()
    ScraperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
