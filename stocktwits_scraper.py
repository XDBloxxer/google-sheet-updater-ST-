import sys
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def configure_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Use the path configured in the workflow
    driver_service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver


def scrape_trending_stocks():
    url = "https://stocktwits.com/sentiment"
    driver = configure_driver()
    driver.get(url)

    try:
        driver.implicitly_wait(10)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        stocks = []

        stock_elements = soup.find_all("div", class_="st_3hZTfnrS st_3aQjLDgp")
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
    url = "https://stocktwits.com/markets/calendar"
    driver = configure_driver()
    driver.get(url)

    try:
        driver.implicitly_wait(10)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        earnings = []

        earnings_elements = soup.find_all("div", class_="earnings-class-name")
        for element in earnings_elements:
            company = element.find("span", class_="company-class-name").text
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
    if len(sys.argv) < 2:
        print("Usage: python stocktwits_scraper.py <1|2>")
        print("1: Scrape Trending Stocks")
        print("2: Scrape Earnings Calendar")
        sys.exit(1)

    choice = sys.argv[1]

    if choice == "1":
        stocks = scrape_trending_stocks()
        print(json.dumps(stocks, indent=4))
    elif choice == "2":
        earnings = scrape_earnings()
        print(json.dumps(earnings, indent=4))
    else:
        print("Invalid choice. Use '1' for Trending Stocks or '2' for Earnings Calendar.")
        sys.exit(1)

if __name__ == "__main__":
    main()