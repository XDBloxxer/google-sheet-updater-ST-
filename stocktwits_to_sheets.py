import requests
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets API credentials
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON')), scope)
    client = gspread.authorize(creds)
    return client

# Fetch trending stocks from StockTwits API
def get_trending_stocks():
    url = "https://api.stocktwits.com/api/2/streams/summary.json"
    response = requests.get(url)
    data = response.json()
    
    # Extract only the trending stock symbols and names
    stocks = []
    for symbol in data['symbols']:
        stocks.append({
            'symbol': symbol['symbol'],
            'name': symbol['name']
        })
    return stocks

# Update Google Sheets with the trending stocks data
def update_google_sheets(sheet_name, stocks):
    client = authenticate_google_sheets()
    sheet = client.open("Flux Capacitor").worksheet("Trending Stocks")  # Open the file and select the sheet "Trending Stocks"
    sheet.clear()  # Clear existing content
    
    # Adding headers to the sheet
    sheet.append_row(["Symbol", "Name"])
    
    # Adding stocks data
    for stock in stocks:
        sheet.append_row([stock['symbol'], stock['name']])

# Main function
if __name__ == "__main__":
    trending_stocks = get_trending_stocks()
    if trending_stocks:
        update_google_sheets("Trending Stocks", trending_stocks)  # Update the "Trending Stocks" sheet in the file
        print("Google Sheets updated successfully with trending stocks!")
    else:
        print("No trending stocks found.")
