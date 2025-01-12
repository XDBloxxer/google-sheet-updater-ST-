import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Function to scrape earnings data
def earnings():
    # Set up headless Chrome to avoid opening the browser window
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    # Launch Chrome with the options
    chrome = webdriver.Chrome(options=options)

    # Go to the earnings calendar page
    chrome.get("https://stocktwits.com/markets/calendar")
    
    # Get the page source (HTML content)
    htmlContent = chrome.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(htmlContent, "html.parser")

    # Find all earnings rows
    earnings = soup.find_all("div", {"role": "row"})
    companyEarnings = []

    # Iterate through the earnings data, skipping the header row
    for earning in earnings[1:]:
        company = earning.find_all("p")
        symbol = company[0].text
        name = company[1].text
        price = earning.find("div", {"class": "EarningsTable_priceCell__Sxx1_"}).text

        # Append the extracted data to the list
        companyEarnings.append({
            "Symbol": symbol,
            "Company Name": name,
            "Price": price
        })

    # Save the earnings data as a JSON file
    with open("earnings.json", "w") as earningsFile:
        json.dump(companyEarnings, earningsFile, indent=4, ensure_ascii=False)

    # Close the Chrome browser instance
    chrome.quit()

# Function to extract data based on user input
def extract():
    # Ask user what data they want to scrape
    query = "3"
    # If the user selects earnings, call the earnings() function
    if query == "4":
        earnings()
    elif query == "0":
        return
    else:
        # Define the URLs for the other options (top gainers, top losers, trending stocks)
        match int(query):
            case 1:
                url = "https://api.stocktwits.com/api/2/symbols/stats/top_gainers.json?regions=US"
                name = "topGainers"
            case 2:
                url = "https://api.stocktwits.com/api/2/symbols/stats/top_losers.json?regions=US"
                name = "topLosers"
            case 3:
                url = "https://api-gw-prd.stocktwits.com/rankings/api/v1/rankings?identifier=US&amp;identifier-type=exchange-set&amp;limit=15&amp;page-num=1&amp;type=ts"
                name = "trending"

        # Send a GET request to the selected URL
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        # Parse the response as JSON
        responseJson = json.loads(response.text)

        # Save the data as a JSON file
        with open(f"{name}.json", "w") as jsonFile:
            json.dump(responseJson, jsonFile, indent=4)

    # Ask if the user wants to continue
    more = "no"
    if more.lower() == "yes":
        extract()
    else:
        return

# Main entry point of the script
if __name__ == "__main__":
    extract()
