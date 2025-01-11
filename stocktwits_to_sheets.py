import os
import json
import gspread
from google.oauth2.service_account import Credentials
import requests
from bs4 import BeautifulSoup

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

# Set headers to avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send GET request to the Stocktwits page
response = requests.get(url, headers=headers)

# Check if the response is successful (status code 200)
if response.status_code == 200:
    # Parse the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Debugging: Print the raw HTML to verify the structure
    print("Raw HTML content:")
    print(soup.prettify()[:1000])  # Print first 1000 characters for inspection

    # Find all the stock symbols (You may need to update this based on the HTML structure)
    trending_stocks = []
    for div in soup.find_all("div", {"class": "symbol"}):
        symbol = div.get_text().strip()  # Extract the symbol text
        trending_stocks.append(symbol)

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
else:
    print(f"Failed to fetch data: {response.status_code}")
