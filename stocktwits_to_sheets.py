import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def configure_driver():
    """
    Configures the Selenium WebDriver with headless mode.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver_service = Service("/path/to/chromedriver")  # Replace with the actual path to chromedriver
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver

def scrape_trending_stocks():
    """
    Scrapes the trending stocks data from StockTwits' trending page.
    """
    url = "https://stocktwits.com/sentiment"
    driver = configure_driver()
    driver.get(url)

    try:
        # Wait for the page to load fully
        driver.implicitly_wait(10)
        html_content = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        stocks = []

        # Locate trending stocks in the source code
        stock_elements = soup.find_all("div", class_="st_3hZTfnrS st_3aQjLDgp")  # Adjust this class as per StockTwits' structure
        for element in stock_elements:
            stock_symbol = element.find("span", class_="st_FXUdnqkF").text
            sentiment = element.find("div", class_="st_3czg6OJD").text.strip() if element.find("div", class_="st_3czg6OJD") else "N/A"
            stocks.append({
                "symbol": stock_symbol,
                "sentiment": sentiment
            })

        driver.quit()
        return stocks

    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return []

def scrape_earnings():
    """
    Scrapes the earnings calendar data from StockTwits' calendar page.
    """
    url = "https://stocktwits.com/markets/calendar"
    driver = configure_driver()
    driver.get(url)

    try:
        # Wait for the page to load fully
        driver.implicitly_wait(10)
        html_content = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        earnings = []

        # Locate earnings data in the source code
        earnings_elements = soup.find_all("div", class_="earnings-class-name")  # Replace 'earnings-class-name' with the correct class
        for element in earnings_elements:
            company = element.find("span", class_="company-class-name").text  # Replace class names as per StockTwits
            date = element.find("span", class_="date-class-name").text.strip() if element.find("span", class_="date-class-name") else "N/A"
            earnings.append({
                "company": company,
                "date": date
            })

        driver.quit()
        return earnings

    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return []

def main():
    """
    Main function to scrape data from StockTwits.
    """
    print("Choose what to scrape:")
    print("1. Trending Stocks")
    print("2. Earnings Calendar")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        stocks = scrape_trending_stocks()
        print(json.dumps(stocks, indent=4))
    elif choice == "2":
        earnings = scrape_earnings()
        print(json.dumps(earnings, indent=4))
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
