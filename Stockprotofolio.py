import requests

# Replace with your Alpha Vantage API key
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'

def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if "Time Series (1min)" not in data:
        return None
    latest_time = sorted(data["Time Series (1min)"].keys())[0]
    latest_price = data["Time Series (1min)"][latest_time]["4. close"]
    return float(latest_price)

class StockPortfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, shares):
        if symbol in self.stocks:
            self.stocks[symbol] += shares
        else:
            self.stocks[symbol] = shares

    def remove_stock(self, symbol, shares):
        if symbol in self.stocks:
            if self.stocks[symbol] > shares:
                self.stocks[symbol] -= shares
            elif self.stocks[symbol] == shares:
                del self.stocks[symbol]
            else:
                print(f"Error: You don't own that many shares of {symbol}.")
        else:
            print(f"Error: You don't own any shares of {symbol}.")

    def view_portfolio(self):
        total_value = 0
        print("\nYour Stock Portfolio:")
        for symbol, shares in self.stocks.items():
            price = get_stock_price(symbol)
            if price:
                value = price * shares
                total_value += value
                print(f"{symbol}: {shares} shares @ ${price:.2f} each = ${value:.2f}")
            else:
                print(f"{symbol}: Unable to retrieve price.")
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")

def main():
    portfolio = StockPortfolio()
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.remove_stock(symbol, shares)
        elif choice == '3':
            portfolio.view_portfolio()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
