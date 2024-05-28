from tkinter import *
import gui
import news
import stock


def main():
    stock_obj = stock.Stock()
    news_obj = news.News()
    window = Tk()
    window.title("Stock and News Application")

    gui_obj = gui.Gui(stock_obj, news_obj, window)

    window.mainloop()


if __name__ == "__main__":
    main()