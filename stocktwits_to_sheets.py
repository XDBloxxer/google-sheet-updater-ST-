import requests
from bs4 import BeautifulSoup

# Function to get trending stocks from StockTwits
def get_trending_stocks():
    url = "https://stocktwits.com/trending"  # Trending page URL
    
    # Send HTTP request to get the page content
    print(f"Requesting: {url}")
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Page successfully retrieved.")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find trending stocks. Inspect the HTML structure to locate them.
        trending_stocks = []
        
        # Look for the element containing trending symbols. StockTwits usually uses <a> or <div> tags.
        for symbol_tag in soup.find_all('a', href=True):  # Checking links to symbols
            href = symbol_tag['href']
            if "/symbols/" in href:  # Filter out non-stock related links
                symbol = href.split('/')[-1]
                trending_stocks.append(symbol)
        
        if trending_stocks:
            print(f"Trending Stocks: {trending_stocks}")
        else:
            print("No trending stocks found.")
        
        return trending_stocks
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

# Run the function to get trending stocks
if __name__ == "__main__":
    trending_stocks = get_trending_stocks()
    if trending_stocks:
        print(f"Trending Stocks: {trending_stocks}")
    else:
        print("No trending stocks found.")
