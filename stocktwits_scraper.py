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

# Function to extract data based on user input
def extract():
    # Directly setting query value (no input needed)
    query = "3"  # Example: scrape trending stocks (set manually)
    
    print("Starting the scraping process...")

    trending_stocks = []  # Initialize an empty list to store trending stocks data
    
    if query == "4":
        earnings()  # This is not relevant for trending stocks
    elif query == "0":
        return trending_stocks
    else:
        match int(query):
            case 1:
                url = "https://api.stocktwits.com/api/2/symbols/stats/top_gainers.json?regions=US"
                name = "topGainers"
            case 2:
                url = "https://api.stocktwits.com/api/2/symbols/stats/top_losers.json?regions=US"
                name = "topLosers"
            case 3:
                # Corrected URL for trending stocks
                url = "https://api-gw-prd.stocktwits.com/rankings/api/v1/rankings?identifier=ALL&identifier-type=exchange-set&limit=100&page-num=1&type=ts"
                name = "trending"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        print(f"Fetching data from {url}...")
        response = requests.get(url, headers=headers)
        
        # Debugging response
        if response.status_code == 200:
            print(f"Successfully fetched data for {name}.")
            responseJson = response.json()

            # Output the raw data for verification
            print(f"Data for {name}:")
            print(json.dumps(responseJson, indent=4))

            # Extract relevant trending stocks data (modify this based on the API response structure)
            if 'data' in responseJson:  # Assuming the API response has a 'data' key
                for stock in responseJson['data']:
                    trending_stocks.append({
                        "symbol": stock.get("symbol", "N/A"),
                        "name": stock.get("name", "N/A")
                    })

            # Debugging: Check if we have any trending stocks
            print(f"Trending stocks data: {trending_stocks}")
                
            # Save the response JSON to a file
            with open(f"{name}.json", "w") as jsonFile:
                json.dump(responseJson, jsonFile, indent=4)
                print(f"Saved data to {name}.json")
        else:
            print(f"Failed to fetch data for {name}, status code: {response.status_code}")
    
    return trending_stocks  # Return the trending stocks data

def populate_google_sheet(trending_stocks):
    if not trending_stocks:
        print("No data to populate in the Google Sheet.")
        return

    print("Starting to populate Google Sheet...")
    
    try:
        # Debug: Verify Google Sheet access
        print(f"Accessing Google Sheet: {sheet.title}")
        
        # Prepare data to insert
        sheet_data = []
        for stock in trending_stocks:
            symbol = stock.get('symbol', 'N/A')
            name = stock.get('name', 'N/A')
            sheet_data.append([symbol, name])

        print(f"Prepared data for insertion: {sheet_data}")
        
        if not sheet_data:
            print("No data to write to the sheet. Exiting.")
            return

        # Debug: Clear the sheet before inserting (optional)
        print("Clearing the sheet...")
        sheet.clear()
        print("Sheet cleared.")

        # Insert the data
        print("Inserting data into the sheet...")
        sheet.insert_rows(sheet_data, row=2)
        print(f"Successfully populated the sheet with {len(sheet_data)} rows.")

    except Exception as e:
        print(f"Error in populating Google Sheet: {e}")


# Main function to handle scraping and Google Sheets update
def main():
    print("Starting the main process...")
    # Get trending stocks data
    trending_stocks = extract()

    # Populate Google Sheets with trending stocks data
    if trending_stocks:
        populate_google_sheet(trending_stocks)
    else:
        print("No trending stocks data found.")

# Entry point of the script
if __name__ == "__main__":
    main()
