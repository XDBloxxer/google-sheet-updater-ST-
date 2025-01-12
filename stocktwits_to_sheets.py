import requests

def get_trending_stocks():
    url = "https://api.stocktwits.com/api/2/streams/trending.json"  # API URL for trending stocks
    print(f"Request URL: {url}")  # Print the URL to ensure it's the correct one
    response = requests.get(url)
    
    # Check the status code of the response
    print(f"Status Code: {response.status_code}")  # Status code of the response
    if response.status_code == 200:
        try:
            data = response.json()
            print("Full Response Data:")
            print(data)  # Print full response data to understand its structure

            trending_stocks = []
            if 'symbols' in data:
                for stock in data['symbols']:
                    trending_stocks.append(stock['symbol'])
                print(f"Trending Stocks: {trending_stocks}")
            else:
                print("No 'symbols' key found in the response.")
            
            return trending_stocks
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            return []
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

# Run the function to see the output
if __name__ == "__main__":
    trending_stocks = get_trending_stocks()
    if trending_stocks:
        print(f"Trending Stocks: {trending_stocks}")
    else:
        print("No trending stocks found.")
