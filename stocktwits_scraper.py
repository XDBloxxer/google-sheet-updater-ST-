import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Function to configure the Selenium WebDriver with necessary options
def configure_driver():
    options = Options()
    options.add_argument('--headless')  # Headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    chrome_bin = os.getenv("CHROME_BIN")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
    
    if not chrome_bin or not chromedriver_path:
        raise EnvironmentError("Chromium or Chromedriver paths are not set.")
    
    # Set the path to chromedriver
    service = Service(executable_path=chromedriver_path)
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Function to scrape trending stocks from StockTwits
def scrape_trending_stocks():
    print("Scraping trending stocks...")
    
    driver = configure_driver()
    driver.get("https://stocktwits.com/")
    
    # Allow page to load
    time.sleep(3)
    
    # Get the page source after it's fully loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all trending stocks (you may need to adjust this part based on StockTwits structure)
    trending_stocks = []
    stock_elements = soup.find_all('a', {'class': 'trending-stocks__ticker'})  # Adjust class or tag based on actual structure
    
    for element in stock_elements:
        stock_symbol = element.text.strip()
        trending_stocks.append(stock_symbol)
    
    driver.quit()
    
    if trending_stocks:
        print("Trending Stocks Found:")
        for stock in trending_stocks:
            print(stock)
    else:
        print("No trending stocks found.")

# Main function to run the script
def main():
    if len(os.sys.argv) > 1:
        argument = os.sys.argv[1]
        print(f"Argument passed: {argument}")
    else:
        print("No argument passed.")
    
    scrape_trending_stocks()

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
