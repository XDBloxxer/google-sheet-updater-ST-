import os
import json
import gspread
from google.oauth2.service_account import Credentials
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Set Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure it's headless
chrome_options.add_argument("--no-sandbox")  # Prevents issues in CI environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents issues with shared memory
chrome_options.add_argument("--remote-debugging-port=9222")  # Ensure debugging is enabled

# Set up WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Google Sheets credentials
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load the Google credentials from the environment variable
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

if GOOGLE_CREDENTIALS_JSON is None:
    raise ValueError("GOOGLE_CREDENTIALS_JSON environment variable is not set.")

# Create credentials from the JSON string
creds = Credentials.from_service_account_info(json.loads(GOOGLE_CREDENTIALS_JSON), scopes=SCOPE)

# Authorize the Google Sheets client
client = gspread.authorize(creds)

# Open the Google Sheet
SPREADSHEET_NAME = 'Flux Capacitor'
sheet = client.open(SPREADSHEET_NAME).worksheet("Trending Stocks")

# Stocktwits trending page URL
url = "https://stocktwits.com/top_stocks"

# Set up Selenium WebDriver (Chrome in this case)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Visit the StockTwits trending page
driver.get(url)

# Wait for the page to fully load
time.sleep(5)  # Adjust sleep time based on your internet speed

# Find all the stock symbols (adjust the selector based on the page structure)
# Inspect the page to get the right class or HTML structure for the stock symbols
elements = driver.find_elements(By.CSS_SELECTOR, ".symbol")  # Adjust CSS selector accordingly

# Extract stock symbols
trending_stocks = [element.text for element in elements]

# Debugging: Print out the list of trending stocks
print("Trending Stocks Extracted:")
print(trending_stocks)

# If there are trending stocks, update the Google Sheet
if trending_stocks:
    for i, symbol in enumerate(trending_stocks, start=2):  # Start at row 2 to avoid overwriting headers
        sheet.update_cell(i, 1, symbol)  # Update the first column with stock symbols
    print(f"Updated {len(trending_stocks)} stocks to Google Sheets.")
else:
    print("No trending stocks found.")

# Close the browser after the task is complete
driver.quit()
