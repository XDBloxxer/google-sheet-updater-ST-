import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_trending_stocks():
    # Automatically install the required version of chromedriver
    chromedriver_autoinstaller.install()

    # Setup options for headless browsing (no GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment this if running headless

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Define the URL for StockTwits sentiment page
    url = "https://stocktwits.com/sentiment"

    # Open the page with Selenium
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(5)

    # Extract the trending stocks (adjust the selector if necessary)
    trending_stocks = []

    try:
        # Find elements containing the stock symbols
        stock_elements = driver.find_elements(By.CSS_SELECTOR, "span.symbol")
        
        # Loop through the found elements and extract text (tickers)
        for stock in stock_elements:
            trending_stocks.append(stock.text)
    except Exception as e:
        print(f"Error while scraping: {e}")
    
    # Close the WebDriver after scraping
    driver.quit()

    # Return the list of trending stocks
    if trending_stocks:
        return trending_stocks
    else:
        print("No trending stocks found.")
        return None

if __name__ == "__main__":
    stocks = get_trending_stocks()
    if stocks:
        print("Trending Stocks:", stocks)
    else:
        print("No trending stocks found.")
