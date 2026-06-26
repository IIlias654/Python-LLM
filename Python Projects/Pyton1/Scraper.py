from playwright.sync_api import sync_playwright
import datetime
import time
from Database import save_to_database


URL = "https://www.ai-fitness.de/studios/augsburg-haunstetten"
SELECTOR = "body > main > section.studio-occupancy-wrapper > div > div > div > div.occupancy-spots__text.MuiBox-root.css-0"
INTERVAL_MINUTES = 10

def scrape_occupancy(url: str) -> str | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        try:
            page.wait_for_selector(SELECTOR, timeout=10_000)
        except Exception:
            print("Occupancy element did not appear within 10 seconds.")
            browser.close()
            return None
        value = page.eval_on_selector(SELECTOR, "el => el.textContent")
        browser.close()
        return value.strip() if value else None


def main():
    occupancy_log: dict[str, str] = {}

    print(f"Polling every {INTERVAL_MINUTES} minutes. Press Ctrl+C to stop.\n")
    while True:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = scrape_occupancy(URL)
        if result is not None:
            value = result.replace("Belegt:","").replace("%", "").strip()
            occupancy_log[timestamp] = value
            print(f"[{timestamp}] Occupancy: {value}")
            save_to_database(occupancy_log)
        else:
            occupancy_log[timestamp] = "N/A"
            print(f"[{timestamp}] Could not retrieve occupancy value.")

        print(f"\nLog so far ({len(occupancy_log)} entries):")
        for ts, val in occupancy_log.items():
            print(f"  {ts}: {val}")
        print(f"\nNext check in {INTERVAL_MINUTES} minutes...\n")

        time.sleep(INTERVAL_MINUTES * 60)


if __name__ == "__main__":
    main()
