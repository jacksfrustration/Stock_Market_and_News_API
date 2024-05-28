from tkinter import messagebox
import requests
import webbrowser

class Stock:
    STOCK_ENDPOINT = "https://www.alphavantage.co/query"
    STOCK_API_KEY = "9UCARY75GSQEK2KX"

    def __init__(self):
        pass

    def check_stock_prices(self, comp_name, company_data):
        """
        Check stock prices for a given company name.

        This method checks if the company name exists in the provided company data.
        If it exists, it retrieves the corresponding symbol and uses it to fetch stock information
        for the latest two dates from the Alpha Vantage API. It then calculates the percentage
        difference between the two dates' closing prices and displays the information.

        Parameters:
        comp_name (str): The name of the company to search for.
        company_data (list): A list of dictionaries containing company names and symbols.
        """
        if not comp_name:
            messagebox.showerror(title="Error", message="You have not entered a company name to search for.")
            return

        company_symbol = None
        for data in company_data:
            if data["name"] == comp_name:
                company_symbol = data["symbol"]
                break

        if not company_symbol:
            messagebox.showerror(title="Error", message="Company name not found.")
            return

        stock_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": company_symbol,
            "apikey": Stock.STOCK_API_KEY
        }
        stock_response = requests.get(Stock.STOCK_ENDPOINT, params=stock_params)

        if stock_response.status_code != 200:
            if messagebox.askokcancel(title="HTTP Status Code Error",
                                      message=f"HTTP status code {stock_response.status_code}. Would you like to search for its meaning?"):
                url = f"https://www.google.com/search?q=http+status+codes+{stock_response.status_code}"
                webbrowser.open(url)
            return

        try:
            time_series = stock_response.json()["Time Series (Daily)"]
            dates = list(time_series.keys())
            yesterdays_data = time_series[dates[0]]
            day_before_data = time_series[dates[1]]

            closing_price_yesterday = float(yesterdays_data['4. close'])
            closing_price_day_before = float(day_before_data['4. close'])
            diff_percentage = round((closing_price_yesterday / closing_price_day_before - 1) * 100, 2)

            if diff_percentage < 0:
                change_type = "decrease"
            else:
                change_type = "increase"

            messagebox.showinfo(
                title=f"{dates[0]} - {dates[1]} Stock Prices",
                message=f"Yesterday's closing price: ${closing_price_yesterday:.2f}\n"
                        f"Day before's closing price: ${closing_price_day_before:.2f}\n"
                        f"There was a {abs(diff_percentage):.2f}% {change_type} between the two dates"
            )

        except KeyError:
            messagebox.showerror(title="Error", message="Error retrieving stock data from response.")