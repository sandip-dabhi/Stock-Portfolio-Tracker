import requests
from prettytable import PrettyTable

# Define your API key from a financial data provider (e.g., Alpha Vantage)
API_KEY = 'your_api_key_here'

# Initialize an empty portfolio
portfolio = {}

def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    try:
        latest_close = list(data['Time Series (1min)'].values())[0]['4. close']
        return float(latest_close)
    except KeyError:
        print(f"Could not retrieve data for {symbol}")
        return None

def add_stock(symbol, shares):
    if symbol in portfolio:
        portfolio[symbol] += shares
    else:
        portfolio[symbol] = shares
    print(f"Added {shares} shares of {symbol} to your portfolio.")

def remove_stock(symbol, shares):
    if symbol in portfolio:
        if portfolio[symbol] >= shares:
            portfolio[symbol] -= shares
            if portfolio[symbol] == 0:
                del portfolio[symbol]
            print(f"Removed {shares} shares of {symbol} from your portfolio.")
        else:
            print(f"Not enough shares of {symbol} to remove.")
    else:
        print(f"{symbol} not found in your portfolio.")

def display_portfolio():
    table = PrettyTable()
    table.field_names = ["Stock", "Shares", "Current Price", "Total Value"]
    total_portfolio_value = 0
    for symbol, shares in portfolio.items():
        price = get_stock_price(symbol)
        if price is not None:
            total_value = shares * price
            table.add_row([symbol, shares, f"${price:.2f}", f"${total_value:.2f}"])
            total_portfolio_value += total_value
    table.add_row(["", "", "Total Portfolio Value", f"${total_portfolio_value:.2f}"])
    print(table)

def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Display Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            add_stock(symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            remove_stock(symbol, shares)
        elif choice == '3':
            display_portfolio()
        elif choice == '4':
            print("Exiting the tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
