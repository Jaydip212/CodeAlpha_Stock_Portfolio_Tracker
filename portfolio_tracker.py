import pandas as pd
import requests
from tabulate import tabulate

class PortfolioTracker:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)

    def add_stock(self, symbol, quantity, purchase_price):
        new_row = {"symbol": symbol, "quantity": quantity, "purchase_price": purchase_price}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.df.to_csv(self.csv_file, index=False)

    def remove_stock(self, symbol):
        self.df = self.df[self.df["symbol"] != symbol]
        self.df.to_csv(self.csv_file, index=False)

def get_stock_price(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return float(data["Global Quote"]["05. price"])

def calculate_portfolio_value(api_key):
    portfolio = pd.read_csv("portfolio.csv")
    total_value = 0
    for _, row in portfolio.iterrows():
        current_price = get_stock_price(row["symbol"], api_key)
        total_value += current_price * row["quantity"]
    return total_value

def show_portfolio(api_key):
    portfolio = pd.read_csv("portfolio.csv")
    data = []
    for _, row in portfolio.iterrows():
        current_price = get_stock_price(row["symbol"], api_key)
        profit_loss = (current_price - row["purchase_price"]) * row["quantity"]
        data.append([row["symbol"], row["quantity"], row["purchase_price"], current_price, profit_loss])
    print(tabulate(data, headers=["Symbol", "Qty", "Buy Price", "Current Price", "P/L"]))

if __name__ == "__main__":
    API_KEY = "OBPGFEPAT5SU0RUT"  # Alpha Vantage API Key 
    tracker = PortfolioTracker("portfolio.csv")
    tracker.add_stock("GOOGL", 5, 2500)
    tracker.remove_stock("TSLA")
    show_portfolio(API_KEY)
    print("Total Portfolio Value:", calculate_portfolio_value(API_KEY))
