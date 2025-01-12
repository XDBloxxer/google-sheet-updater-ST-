import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


# Google Sheets API setup
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        GOOGLE_CREDENTIALS_JSON, scope)
    client = gspread.authorize(creds)
    return client


# Function to scrape trending stocks from StockTwits
def get_trending_stocks():
    url = 'https://stocktwits.com/symbols'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    trending_stocks = []
    
    # Extracting the trending symbols
    # We need to find the elements containing the trending symbols
    symbols = soup.find_all('a', class_='twtr-ticker')
    
    for symbol in symbols:
        symbol_text = symbol.get_text(strip=True)
        if symbol_text:
            trending_stocks.append(symbol_text)
    
    return trending_stocks


# Function to update the Google Sheets
def update_google_sheet(client, trending_stocks):
    sheet = client.open("Flux Capacitor").worksheet("Trending Stocks")

    # Clear the existing content
    sheet.clear()

    # Add headers
    sheet.append_row(['Trending Stock Symbol'])
    
    # Add the trending stocks to the sheet
    for stock in trending_stocks:
        sheet.append_row([stock])
    print(f"Successfully updated the sheet with {len(trending_stocks)} trending stocks.")


# Main function
def main():
    # Authenticate and get the client
    client = authenticate_google_sheets()

    # Scrape the trending stocks
    trending_stocks = get_trending_stocks()
    
    if trending_stocks:
        # Update the Google Sheets with the trending stocks
        update_google_sheet(client, trending_stocks)
    else:
        print("No trending stocks found.")

# Run the script
if __name__ == "__main__":
    main()
