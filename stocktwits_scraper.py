import requests
import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import gspread
from google.oauth2.service_account import Credentials

# Set up Google Sheets API credentials
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Load the Google credentials from the environment variable
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

if GOOGLE_CREDENTIALS_JSON is None:
    raise ValueError("GOOGLE_CREDENTIALS_JSON environment variable is not set.")

# Create credentials from the JSON string
creds = Credentials.from_service_account_info(
    json.loads(GOOGLE_CREDENTIALS_JSON), scopes=SCOPE
)

# Authorize the Google Sheets client
client = gspread.authorize(creds)

# Open the Google Sheet
SPREADSHEET_NAME = "Flux Capacitor"
sheet = client.open(SPREADSHEET_NAME).worksheet("Trending Stocks")


# Function to fetch trending stocks data
def extract():
    print("Starting the scraping process...")
    query = "3"  # Hardcoded for trending stocks

    match int(query):
        case 3:
            url = (
                "https://api-gw-prd.stocktwits.com/rankings/api/v1/rankings?"
                "identifier=ALL&identifier-type=exchange-set&limit=100&page-num=1&type=ts"
            )
            name = "trending"

    headers = {"User-Agent": "Mozilla/5.0"}
    print(f"Fetching data from {url}...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Successfully fetched data for {name}.")
        response_json = response.json()

        # Parse the relevant data
        trending_stocks = [
            {
                "symbol": stock.get("symbol", "N/A"),
                "name": stock.get("name", "N/A"),
            }
            for stock in response_json.get("data", {}).get("rows", [])
        ]

        print(f"Number of stocks fetched: {len(trending_stocks)}")
        if trending_stocks:
            print(f"Sample stock: {trending_stocks[0]}")

        return trending_stocks
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        return []


# Function to populate Google Sheets with trending stocks
def populate_google_sheet(trending_stocks):
    if not trending_stocks:
        print("No data to populate in the Google Sheet.")
        return

    print("Starting to populate Google Sheet...")

    try:
        # Verify Google Sheet access
        print(f"Accessing Google Sheet: {sheet.title}")

        # Prepare and log only a summary of the data
        sheet_data = [
            [stock.get("symbol", "N/A"), stock.get("name", "N/A")]
            for stock in trending_stocks
        ]
        print(f"Prepared {len(sheet_data)} rows for insertion.")

        # Insert test data to confirm connection
        print("Inserting test data for validation...")
        test_row = [["TEST", "ROW"]]
        sheet.insert_rows(test_row, row=2)
        print("Test row inserted successfully.")

        # Clear the sheet and insert actual data
        print("Clearing the sheet...")
        sheet.clear()
        print("Sheet cleared. Inserting stock data...")

        # Insert stock data
        sheet.insert_rows(sheet_data, row=2)
        print(f"Inserted {len(sheet_data)} rows into the sheet.")

    except Exception as e:
        print(f"Error populating Google Sheet: {e}")


# Main function to handle scraping and Google Sheets update
def main():
    print("Starting script...")
    print("Fetching trending stocks...")

    trending_stocks = extract()

    if not trending_stocks:
        print("No trending stocks data fetched. Exiting...")
        return

    print("Attempting to populate Google Sheet...")
    populate_google_sheet(trending_stocks)
    print("Script finished.")


# Entry point of the script
if __name__ == "__main__":
    main()
