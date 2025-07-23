# 🗓️ Event Automation

This project automates scraping of Indian/South Asian-themed events from [Eventbrite](https://www.eventbrite.com/) and appends only new, recent ones to a newline-delimited JSON file (`latest_indian_events.ndjson`). It avoids duplicates, filters old events, and runs completely headless in the background.

---

## 🚀 Features

- ✅ Scrapes events using keywords like "indian", "desi", "bollywood", etc.
- ✅ Checks multiple major U.S. cities
- ✅ Keeps only events from the past 7 days
- ✅ Appends to an NDJSON file — no memory-heavy file loads
- ✅ Skips duplicates using title + date
- ✅ Headless Chrome via Selenium
- ✅ No ChromeDriver setup needed (auto-handled with `webdriver-manager`)

---

## 📁 File Structure

event_automation/
├── newautomation.py # The main scraping script
├── requirements.txt # Python dependencies
└── README.md # This file

---

## 📦 Requirements

- Python 3.8 or later
- Google Chrome (installed on system)

---

## 🛠️ Setup Instructions

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/event_automation.git
   cd event_automation
2. **Install dependencies**:
    pip install -r requirements.txt

3. **Run the script**:
   python newautomation.py

🔹 Output will be saved in a file named latest_indian_events.ndjson, with one JSON object per line.

⚠️ Notes
✅ Only events from the past 7 days are stored.

✅ Chrome must be installed (used headlessly).

⚠️ This script avoids loading the full JSON to keep memory usage low.

🔁 You can run this multiple times — it won't save duplicates.

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.


   
