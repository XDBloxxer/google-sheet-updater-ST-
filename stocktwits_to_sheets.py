import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    # Explicit wait for the elements containing stock tickers
    try:
        # Wait until the trending stocks are visible on the page (adjust selector as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.symbol"))
        )

        # Extract the trending stocks
        trending_stocks = []

        # Find elements containing the stock symbols
        stock_elements = driver.find_elements(By.CSS_SELECTOR, "span.symbol")
        
        # Loop through the found elements and extract text (tickers)
        for stock in stock_elements:
            trending_stocks.append(stock.text)

        # Check if stocks are found
        if trending_stocks:
            return trending_stocks
        else:
            print("No trending stocks found.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return None
    finally:
        # Close the WebDriver after scraping
        driver.quit()

if __name__ == "__main__":
    stocks = get_trending_stocks()
    if stocks:
        print("Trending Stocks:", stocks)
    else:
        print("No trending stocks found.")
