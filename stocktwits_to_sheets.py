import requests

def get_trending_stocks():
    url = "https://api.stocktwits.com/api/2/streams/trending.json"  # Update if the endpoint is different
    response = requests.get(url)
    
    # Check for response status
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text[:1000]}")  # Print the first 1000 characters of the response
    
    # If status code is OK, then try parsing JSON
    if response.status_code == 200:
        try:
            data = response.json()
            print("Full Response Data:")
            print(data)  # Print full response data to understand its structure

            trending_stocks = []
            # Check if 'symbols' exist and if so, extract stock symbols
            if 'symbols' in data:
                for stock in data['symbols']:
                    trending_stocks.append(stock['symbol'])
            else:
                print("No 'symbols' key found in the response.")
            
            return trending_stocks
        except ValueError:
            print("Error parsing JSON response.")
            return []
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []
