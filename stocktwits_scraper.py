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
        for page_data in data:
            if "response" in page_data and "ranks" in page_data["response"]:
                for rank_data in page_data["response"]["ranks"]:
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
            range="Trending Stocks!A:D"
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
    base_url = "https://api-gw-prd.stocktwits.com/rankings/api/v1/rankings"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    all_data = []
    max_pages = 5  # Fetch data from pages 1 to 5

    print("Fetching trending stocks data...")
    for page_num in range(1, max_pages + 1):
        url = f"{base_url}?identifier=ALL&identifier-type=exchange-set&limit=100&page-num={page_num}&type=ts"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            all_data.append(data)
            print(f"Fetched data for page {page_num}")
        else:
            print(f"Failed to fetch data for page {page_num}, status code: {response.status_code}")
            break
    
    # Save all pages' data to a local JSON file
    with open("trending.json", "w") as jsonFile:
        json.dump(all_data, jsonFile, indent=4)
        print("Saved data to trending.json")
    
    # Update Google Sheet
    if update_google_sheet(all_data):
        print("Successfully updated Google Sheet 'Flux Capacitor'")
    else:
        print("Failed to update Google Sheet")

if __name__ == "__main__":
    extract()
