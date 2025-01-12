import os
import gspread
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from google.oauth2.service_account import Credentials
import time


# Function to scrape earnings data
def earnings():
    # Set up headless Chrome to avoid opening the browser window
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    # Launch Chrome with the options
    chrome = webdriver.Chrome(options=options)

    # Go to the earnings calendar page
    chrome.get("https://stocktwits.com/rankings")
    
    # Get the page source (HTML content)
    htmlContent = chrome.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(htmlContent, "html.parser")

    # Find all earnings rows
    earnings = soup.find_all("div", {"role": "row"})
    companyEarnings = []

    # Iterate through the earnings data, skipping the header row
    for earning in earnings[1:]:
        company = earning.find_all("p")
        symbol = company[0].text
        name = company[1].text
        price = earning.find("div", {"class": "EarningsTable_priceCell__Sxx1_"}).text

        # Append the extracted data to the list
        companyEarnings.append({
            "Symbol": symbol,
            "Company Name": name,
            "Price": price
        })

    # Save the earnings data as a JSON file
    with open("earnings.json", "w") as earningsFile:
        json.dump(companyEarnings, earningsFile, indent=4, ensure_ascii=False)

    # Close the Chrome browser instance
    chrome.quit()

# Function to extract data based on user input
import requests
import json

def earnings():
    # Placeholder for earnings scraping logic
    # For now, we'll just print a message that it's being executed
    print("Earnings function executed (this would scrape earnings information).")
    # You can add your scraping logic here for earnings if needed.

def extract():
    # Directly setting query value (no input needed)
    query = "3"  # Example: scrape trending stocks (set manually)
    
    print("Starting the scraping process...")
    
    if query == "4":
        earnings()
    elif query == "0":
        return
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
        
        if response.status_code == 200:
            print(f"Successfully fetched data for {name}.")
            responseJson = response.json()

            # Output the raw data for verification
            print(f"Data for {name}:")
            print(json.dumps(responseJson, indent=4))

            # Save the response JSON to a file
            with open(f"{name}.json", "w") as jsonFile:
                json.dump(responseJson, jsonFile, indent=4)
                print(f"Saved data to {name}.json")
        else:
            print(f"Failed to fetch data for {name}, status code: {response.status_code}")
    
    # Simulate "Do you want to continue?" prompt, automatically choosing "no"
    more = "no"  # Simulating that user doesn't want to continue

    if more.lower() == "yes":
        extract()  # Restart the process
    else:
        print("Exiting...")

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

def populate_google_sheet(trending_stocks):
    # Authenticate with Google Sheets API
    gc = authenticate_google_sheets()
    
    # Open the Google Sheets file and the 'Trending Stocks' sheet
    sheet = gc.open("Flux Capacitor").worksheet("Trending Stocks")
    
    # Prepare the data to insert
    sheet_data = []
    for stock in trending_stocks:
        symbol = stock.get('symbol', 'N/A')  # Use 'N/A' if symbol is missing
        name = stock.get('name', 'N/A')      # Use 'N/A' if name is missing
        sheet_data.append([symbol, name])
    
    # Write the data to the sheet, starting from row 2 (to keep headers intact)
    sheet.insert_rows(sheet_data, row=2)
    print(f"Populated 'Trending Stocks' sheet with {len(sheet_data)} entries.")

def main():
    # Get trending stocks data
    trending_stocks = get_trending_stocks()

    # Populate the Google Sheets with trending stocks data
    if trending_stocks:
        populate_google_sheet(trending_stocks)
    else:
        print("No trending stocks data found.")

# Entry point of the script
if __name__ == "__main__":
    main()
