import requests
import json
import gspread
from google.auth import exceptions
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.auth import impersonated_credentials

# Function to authenticate Google Sheets API using credentials from GitHub secrets
def authenticate_google_sheets():
    # Read the credentials JSON from the GitHub secrets
    google_credentials = os.getenv('GOOGLE_CREDENTIALS_JSON')

    if google_credentials is None:
        print("Error: Google credentials not found in GitHub secrets.")
        return None

    # Convert the credentials JSON string to a dictionary
    credentials_info = json.loads(google_credentials)

    # Load the credentials from the dictionary
    credentials = Credentials.from_service_account_info(credentials_info)

    # Authenticate and initialize gspread client
    gc = gspread.authorize(credentials)
    return gc

# Function to get trending stock data
def get_trending_stocks():
    url = "https://api-gw-prd.stocktwits.com/rankings/api/v1/rankings?identifier=ALL&identifier-type=exchange-set&limit=100&page-num=1&type=ts"
    headers = {"User-Agent": "Mozilla/5.0"}
    print(f"Fetching data from {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Successfully fetched data for trending stocks.")
        responseJson = response.json()
        return responseJson['data']
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        return []

# Function to populate Google Sheets with trending stocks
def populate_google_sheet(trending_stocks):
    # Authenticate with Google Sheets API
    gc = authenticate_google_sheets()
    
    if not gc:
        return

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

# Main function to handle scraping and Google Sheets update
def main():
    # Get trending stocks data
    trending_stocks = get_trending_stocks()

    # Populate Google Sheets with trending stocks data
    if trending_stocks:
        populate_google_sheet(trending_stocks)
    else:
        print("No trending stocks data found.")

# Entry point of the script
if __name__ == "__main__":
    main()
