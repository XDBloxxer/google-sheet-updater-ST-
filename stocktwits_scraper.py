import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import google.oauth2.service_account as service_account
from googleapiclient.discovery import build
from datetime import datetime

def get_google_credentials():
    """Get Google credentials from GitHub secrets."""
    credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    if not credentials_json:
        raise ValueError("Google credentials not found in environment variables")
    
    credentials_info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return credentials

def update_google_sheet(data):
    """Update Google Sheet with stock data."""
    try:
        credentials = get_google_credentials()
        service = build('sheets', 'v4', credentials=credentials)
        
        spreadsheet_id = "1u7ixhoxCwYo-mUm0mod62Rt-IMBTSX4SOhZbIpQ0Tbw"  # Replace with your actual spreadsheet ID
        range_name = "Trending Stocks!A1"
        
        # Prepare the data for Google Sheets
        # First row is headers
        values = [["Rank", "Symbol", "Company Name", "Price"]]
        
        # Add data rows
        if "response" in data and "ranks" in data["response"]:
            for rank_data in data["response"]["ranks"]:
                stock = rank_data.get("stock", {})
                pricing = rank_data.get("pricing", {})
                values.append([
                    rank_data.get("rank", ""),
                    stock.get("symbol", ""),
                    stock.get("name", ""),
                    pricing.get("price", "")
                ])
        
        body = {
            'values': values
        }
        
        # Clear existing content and update with new data
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range="Trending Stocks!A:D"  # Changed from A:F to A:D since we removed 2 columns
        ).execute()
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Updated {result.get('updatedCells')} cells in Google Sheets")
        return True
    
    except Exception as e:
        print(f"Error updating Google Sheet: {str(e)}")
        return False

def extract():
    print("Fetching all trending stocks...")
    base_url = (
        "https://api-gw-prd.stocktwits.com/rankings/api/v1/rankings?"
        "identifier=ALL&identifier-type=exchange-set&limit=100&page-num={page}&type=ts"
    )
    headers = {"User-Agent": "Mozilla/5.0"}

    all_trending_stocks = []
    page = 1  # Start with the first page

    while True:
        print(f"Fetching page {page}...")
        response = requests.get(base_url.format(page=page), headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch data from page {page}, status code: {response.status_code}")
            break

        try:
            response_json = response.json()
            rows = response_json.get("data", {}).get("rows", [])
            if not rows:
                print(f"No more data on page {page}. Stopping.")
                break
            
            print(f"Fetched {len(rows)} stocks from page {page}.")
            all_trending_stocks.extend(rows)  # Add the current page's data to the full list
            page += 1  # Move to the next page

        except Exception as e:
            print(f"Error parsing JSON response from page {page}: {e}")
            break

    print(f"Total stocks fetched: {len(all_trending_stocks)}")
    return all_trending_stocks

if __name__ == "__main__":
    extract()
