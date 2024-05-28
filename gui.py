from tkinter import *
from tkinter import messagebox
import json
from stock import Stock
from news import News

class Gui:
    def __init__(self, stock_obj, news_obj, window):
        """
        Initialize the GUI with stock and news objects and the main Tkinter window.

        Parameters:
        stock_obj (Stock): The Stock object to fetch stock data.
        news_obj (News): The News object to fetch news data.
        window (Tk): The Tkinter window object.
        """
        self.stock = stock_obj
        self.news = news_obj
        self.window = window

        self.canvas = Canvas(self.window, width=275, height=187)
        self.bg_pic = PhotoImage(file="getty-stock-market-data-3742641520.png")
        self.company_data = self.load_data()
        self.names_list = [datum["name"] for datum in self.company_data]

        self.create_gui()

    def load_data(self):
        """
        Load company data from a JSON file.

        Returns:
        list: A list of dictionaries containing company names and symbols.
        """
        with open("company_id.json", "r") as file:
            data = json.load(file)["data"]

        # Create a new list of dictionaries with only name and symbol
        return [{"name": datum[1], "symbol": datum[2]} for datum in data]

    def create_gui(self):
        """
        Create and configure the GUI components.
        """
        bg = self.canvas.create_image(270, 177, image=self.bg_pic)
        self.canvas.grid(row=0, column=0, columnspan=11)

        Label(text="Enter Company Name: ").grid(row=1, column=0)
        self.company_name_ent = Entry()
        self.company_name_ent.grid(row=1, column=1)

        Button(text="Find Company Name", command=self.find_company_name).grid(row=1, column=2)

        Label(text="Look for").grid(row=1, column=3)
        self.news_results_ent = Entry()
        self.news_results_ent.grid(row=1, column=4)
        Label(text="news article results").grid(row=1, column=5)

        Button(text="Get news articles", command=self.get_news).grid(row=2, column=1, columnspan=2)
        Button(text="Get Yesterday's data", command=self.check_stock_prices).grid(row=2, column=3, columnspan=2)

    def find_company_name(self):
        """
        Find company names that match the search term entered by the user.
        """
        search_term = self.company_name_ent.get().lower()
        self.search_results = [data["name"] for data in self.company_data if search_term in data["name"].lower()]

        if self.search_results:
            for comp_name in self.search_results:
                if messagebox.askokcancel(title="Found Results", message=f"We have found {comp_name}. "
                                                                        f"Would you like to search for "
                                                                        f"stock market data for this company?"):
                    self.company_name_ent.delete(0, END)
                    self.company_name_ent.insert(0, comp_name)
                    break
        else:
            messagebox.showerror(title="Oops", message="Company name not found")

    def get_news(self):
        """
        Get news articles based on the number of results and company name provided by the user.
        """
        try:
            news_results = int(self.news_results_ent.get())
        except ValueError:
            messagebox.showerror(title="Oops", message="You have not entered a valid number for how many news articles you want to find")
            return

        company_name = self.company_name_ent.get()
        if not company_name:
            messagebox.showerror(title="Oops", message="You have not entered a company name! Try again!")
            return

        try:
            self.news.get_news(company_name, news_results)
        except AttributeError as e:
            messagebox.showerror(title="Oops", message=f"An unexpected error occurred: {e}\nPlease try again!")

    def check_stock_prices(self):
        """
        Check stock prices for the company name provided by the user.
        """
        self.stock.check_stock_prices(self.company_name_ent.get(), self.company_data)