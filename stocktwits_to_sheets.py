import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Environment variable for Google Credentials (already set in your environment)
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

# Define the Google Sheets authorization function
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_JSON, scope)
    client = gspread.authorize(creds)
    return client

# Scrape the Stocktwits Trending Stocks (using BeautifulSoup and Selenium as needed)
def get_trending_stocks():
    url = "https://www.stocktwits.com/"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (without opening browser)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    
    # Initialize WebDriver with the ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    # Grab the page source after it has loaded
    page_source = driver.page_source
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    trending_stocks = []

    # This is where you extract the actual trending stocks data
    # This may require you to inspect the HTML structure to grab the right tags/classes
    for stock in soup.find_all('a', {'class': 'st_symbol'}):  # Adjust the class based on actual HTML
        trending_stocks.append(stock.text.strip())

    if not trending_stocks:
        print("No trending stocks found.")
    return trending_stocks

# Main function to orchestrate the process
def main():
    # Authenticate Google Sheets
    client = authenticate_google_sheets()

    # Open the specific sheet by its name
    sheet = client.open("Flux Capacitor").worksheet("Trending Stocks")

    # Get the trending stocks data
    trending_stocks = get_trending_stocks()

    if trending_stocks:
        # Clear the existing data
        sheet.clear()

        # Write the new data into the sheet
        for i, stock in enumerate(trending_stocks, start=1):
            sheet.update_cell(i, 1, stock)
        print(f"Updated the sheet with {len(trending_stocks)} trending stocks.")
    else:
        print("No new trending stocks to update.")

if __name__ == "__main__":
    main()
