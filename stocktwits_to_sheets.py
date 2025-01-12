from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Function to get the trending stocks
def get_trending_stocks():
    # Set up Selenium with headless Chrome browser (no UI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Initialize Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # URL for StockTwits trending page
    url = "https://stocktwits.com/sentiment"
    driver.get(url)
    
    # Give it some time to load (important for dynamically loaded content)
    time.sleep(5)  # Wait for 5 seconds to ensure the page loads
    
    # Get the page source (HTML)
    page_source = driver.page_source
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Look for the elements that contain trending stock symbols (based on the guide)
    trending_stocks = []
    
    # Find all elements containing stock symbols
    # From the page structure, you can find stock symbols inside the 'a' tags with href containing '/symbols/'
    for link in soup.find_all('a', href=True):
        href = link['href']
        if "/symbols/" in href:  # Filter to get only stock symbols
            stock_symbol = href.split('/')[-1]  # Extract the ticker symbol
            trending_stocks.append(stock_symbol)
    
    # Close the browser once done
    driver.quit()
    
    # Return the list of trending stock symbols
    return trending_stocks

# Run the function to get trending stocks
if __name__ == "__main__":
    trending_stocks = get_trending_stocks()
    if trending_stocks:
        print("Trending Stocks:")
        for stock in trending_stocks:
            print(stock)
    else:
        print("No trending stocks found.")
