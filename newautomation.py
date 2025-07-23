import json, os, time
from datetime import datetime, timedelta
import dateparser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

file_path = "latest_indian_events.json"
existing = set()
data = []

# Load existing data
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
        for e in existing_data:
            existing.add((e["title"], e["date_time"]))
else:
    existing_data = []

# Filters
now = datetime.now()
week_ago = now - timedelta(days=7)

def recent(date_text):
    dt = dateparser.parse(date_text, settings={'TIMEZONE': 'US/Eastern'})
    return dt and dt >= week_ago

# Fewer combinations for speed – expand later
keywords = ["indian", "desi"]
cities = ["dallas", "new-york", "san-francisco"]

def fetch(keyword, city):
    url = f"https://www.eventbrite.com/d/{city}/{keyword.replace(' ', '-')}/"
    print(f"🔍 {url}")
    driver.get(url)
    try:
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".event-card")))
        time.sleep(0.5)
        cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='event-card-tracking-layer'] ~ section")

        for card in cards[:6]:  # Limit to top 6 events per combo
            try:
                box = card.find_element(By.XPATH, "./ancestor::div[contains(@class, 'event-card')]")
                title = box.find_element(By.CSS_SELECTOR, "h3").text.strip()
                if not title: continue

                dt_text = box.find_element(By.CSS_SELECTOR, "p.Typography_body-md__487rx").text.strip()
                if not recent(dt_text): continue

                url = box.find_element(By.CSS_SELECTOR, "a.event-card-link").get_attribute("href")
                desc = box.find_element(By.CSS_SELECTOR, "h3").get_attribute("aria-label") or "No description"

                key = (title, dt_text)
                if key in existing: continue
                existing.add(key)

                data.append({
                    "title": title,
                    "date_time": dt_text,
                    "location": city.replace("-", " ").title(),
                    "url": url,
                    "description": desc
                })
            except: continue
    except Exception as e:
        print(f"❌ {city}-{keyword} failed: {e}")

# Run
for kw in keywords:
    for ct in cities:
        fetch(kw, ct)

# Save
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(existing_data + data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Added {len(data)} new events. Total: {len(existing_data) + len(data)}")
driver.quit()
