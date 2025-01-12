import requests

def get_trending_stocks():
    # The URL of the API endpoint (replace this with the actual API URL from the network request)
    api_url = "https://api-gw-prd.stocktwits.com/rankings/api/v1/rankings?identifier=US&amp;identifier-type=exchange-set&amp;limit=15&amp;page-num=1&amp;type=ts"  # Example API, replace with actual API URL

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Make the GET request to the API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        trending_stocks = []

        # Assuming the data contains a list of stock symbols, adjust the path as needed
        for stock in data.get('symbols', []):
            trending_stocks.append(stock['symbol'])

        return trending_stocks
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


if __name__ == "__main__":
    stocks = get_trending_stocks()
    if stocks:
        print("Trending Stocks:", stocks)
    else:
        print("No trending stocks found.")
