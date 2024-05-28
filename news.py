import requests
from tkinter import messagebox
import webbrowser

class News:
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
    NEWS_API_KEY = "bcee3aec44b349f8bf5866d6133849ff"

    def get_news(self, comp_name, news_results):
        """
        Fetches news articles related to a given company name and opens them in the browser.

        Parameters:
        comp_name (str): The name of the company.
        news_results (int): The number of news articles to fetch.
        """
        # Check if the company name is provided
        if not comp_name:
            messagebox.showerror(title="Error", message="Please enter a company name.")
            return

        # Fetch news articles from the News API
        news_params = {
            "apiKey": self.NEWS_API_KEY,
            "q": comp_name,
            "searchIn": "title"
        }
        news_response = requests.get(self.NEWS_ENDPOINT, params=news_params)

        # Handle HTTP errors
        if news_response.status_code != 200:
            self.handle_http_error(news_response.status_code)
            return

        # Extract articles and open them in the browser
        articles = news_response.json().get("articles", [])
        if articles:
            for index,article in enumerate(articles[:news_results]):
                if messagebox.askyesno(title=f"Open Article {index+1}/{news_results}",
                                       message=f"Article Title: {article['title']}\nWould you like to read this article?"):
                    webbrowser.open(article['url'])
        else:
            messagebox.showinfo(title="No News Found", message="No news articles found for the given company.")

    def handle_http_error(self, status_code):
        """
        Handles HTTP errors by showing an error message to the user.

        Parameters:
        status_code (int): The HTTP status code.
        """
        messagebox.showerror(title="HTTP Error", message=f"Failed to fetch news. Status Code: {status_code}")