import re
import os
import time
import argparse
import datetime
import threading
import tkinter as tk
from tkinter import simpledialog
from urllib.parse import urlparse, urljoin

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:

    def __init__(self, auto: bool, no_format: bool):
        self.auto = auto
        self.no_format = no_format
        self.visited_urls = set()

        chrome_options = Options()
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        if self.auto:
            chrome_options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })

    def start(self):
        url = self.get_input_str("URL", "Provide a starting URL\n(Later you can navigate to any page)")
        self.driver.get(url)
        print(self.driver.title)

        if self.auto:
            self.scrape_all_links(url)
        else:
            threading.Thread(target=self.scrape_button_gui, daemon=True).start()

        while True:
            time.sleep(1)

    def scrape_all_links(self, start_url: str):
        '''
        Automatically scrapes all pages starting from the given URL and following internal links
        that belong to the same domain.
        '''
        self.visited_urls.add(start_url)
        self.scrape_page(start_url)

        links_to_visit = self.get_links_on_page(start_url)
        for link in links_to_visit:
            if link not in self.visited_urls:
                self.visited_urls.add(link)
                self.scrape_page(link)

    def scrape_page(self, url: str):
        '''
        Scrapes the page content of a given URL.
        Saves the page as a text file (or full HTML based on no_format setting).
        '''
        self.driver.get(url)
        print(f"Scraping: {url}")

        if self.no_format:
            page_content = self.driver.page_source
            safe_url = re.sub(r'[\\/*?:"<>|]', "_", url)
            filename = f"./scraped_pages/{safe_url}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_full.html"
        else:
            page_text = self.driver.find_element("tag name", "body").text
            safe_url = re.sub(r'[\\/*?:"<>|]', "_", url)
            filename = f"./scraped_pages/{safe_url}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(page_content if self.no_format else page_text)

        print(f"Scraped: {filename}")

    def get_links_on_page(self, url: str):
        '''
        Retrieves all internal links on a page that belong to the same domain.
        '''
        domain = urlparse(url).netloc
        links = set()

        anchor_tags = self.driver.find_elements("tag name", "a")
        for tag in anchor_tags:
            href = tag.get_attribute("href")
            if href:
                parsed_href = urlparse(href)
                if parsed_href.netloc == domain or parsed_href.netloc == '': # Link is within the same domain
                    absolute_url = urljoin(url, href)
                    links.add(absolute_url)

        return links

    def scrape_button_gui(self):
        '''
        Creates a simple tkinter window with a SCRAPE button.
        Always on top, not minimizable. Saves only text content of the current page.
        '''

        root = tk.Tk()
        root.title("Selenium Scraper")
        root.geometry("200x100")
        root.attributes("-topmost", True)
        root.resizable(False, False)

        btn = tk.Button(root, text="SCRAPE", command=lambda: self.scrape_page(self.driver.current_url), font=("Arial", 14), padx=10, pady=5)
        btn.pack(expand=True)

        def prevent_minimize():
            while True:
                if root.state() == "iconic":
                    root.deiconify()
                time.sleep(0.5)

        threading.Thread(target=prevent_minimize, daemon=True).start()

        root.mainloop()


    def get_input_str(self, title: str, prompt: str) -> str:
        '''
        Opens a dialog window and asks the user to input a string.

        :param title: Title of the input dialog window.
        :param prompt: Prompt message for the user.
        :return: The string entered by the user.
        '''
        root = tk.Tk()
        root.withdraw()
        user_input = simpledialog.askstring(title, prompt)
        return user_input


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Web Page Scraper")
    parser.add_argument('--auto', action='store_true', help='Enable automatic scraping mode')
    parser.add_argument('--no-format', action='store_true', help='Disable output formatting')
    args = parser.parse_args()

    scraper = Scraper(args.auto, args.no_format)
    scraper.start()
