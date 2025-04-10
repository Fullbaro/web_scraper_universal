
# Universal Web Page Scraper 🌐

This project provides a universal web page scraper solution, which allows users to scrape the content of any website. The scraper operates within a Chrome window, where you can freely navigate to any page. By pressing a "SCRAPE" button, the entire page content (text and optionally HTML/JS code) is saved locally.

## Features ✨

-   **User-Friendly Interface** 🖱️: A simple GUI allows you to control the scraper easily.
-   **Text Extraction** 📄: Saves the content of the page as plain text, excluding HTML and JavaScript, or as a complete HTML page, based on the configuration.
-   **Automatic Mode** 🤖: When enabled, the scraper can run in headless mode, automatically navigating and scraping multiple pages from a specified URL, saving the content of each page it visits.
-   **Customizable Options** ⚙️:
    -   **No Format**: When enabled, the scraper saves the full HTML and JavaScript code of the page.
    -   **Auto Mode**: Automatically navigates through all the links on a page and scrapes all reachable pages under the original domain.

## Install 💻

### Requirements

-   Python 3.x
-   Chrome browser

Install required pip packages:

```
pip install -r requirements.txt
```

## Usage 🚀

1.  Run the program with **optional** parameters
2.  `python main.py`
    -   **- -auto:** No GUI. After a starting URL provided, automatically finds all links on page and saves each page in **scraped_pages** folder. **WARNING: Can stuck in infinite loop -> Feel free to cancel run with CTR+C**
    -   **- -no-format:** By default it only saves the text content of page. If no-format provided, all html tags and js code saved.
3.  In the popup windows provide a starting URL. Later you can navigate to every page and save its content.
4.  By pressing the SCRAPE button the all data on page gets saved in **scraped_pages** folder.