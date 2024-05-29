import customtkinter as ctk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class Strategy(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pq_loc_dir     = "../tw-stock-screener/database/"
        self.canvas         = None
        self.symbol         = 2330
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        style = ttk.Style()
        
        style.configure("Treeview.Heading", font=("Helvetica", 20))
        style.configure("Treeview", rowheight=50, font=("Helvetica", 20))

        # Configure buttons
        self.factor_dataframe = ttk.Treeview(self, columns=("Factor Name", "Return"), show="headings", style="Treeview")
        self.factor_dataframe.heading("Factor Name", text="Factor Name")
        self.factor_dataframe.heading("Return", text="Return")
        self.factor_dataframe.bind("<ButtonRelease-1>", self.on_factor_click)
        self.factor_dataframe.grid(row=0, column=0, padx=2, pady=2, sticky='n')
        self.insert_factor_tree()

        self.factor_selection_dataframe = ttk.Treeview(self, columns=("Ticker", "Date", "return-to-date"), show="headings", style="Treeview")
        self.factor_selection_dataframe.heading("Ticker", text="Ticker")
        self.factor_selection_dataframe.heading("Date", text="Date")
        self.factor_selection_dataframe.heading("return-to-date", text="return-to-date")
        self.factor_selection_dataframe.bind("<ButtonRelease-1>", self.on_tree_click)
        self.factor_selection_dataframe.grid(row=0, column=1, padx=2, pady=2, sticky='n')

        self.plotting(2330)

        self.textbox = ctk.CTkTextbox(self, width=200, height=200, corner_radius=20)
        self.textbox.grid(row=1, column=1, padx=2, pady=2, sticky='nsew')

    
    def on_factor_click(self, event):
        item = self.factor_dataframe.identify('item', event.x, event.y)
        factor_name = self.factor_dataframe.item(item, "values")[0]
        self.textbox.insert('end', factor_name + '\n')
    def on_tree_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        symbol = self.tree.item(item, "values")[0]
        self.symbol = symbol
        self.plotting(self.symbol1.split(".")[0], column=0)
    def plotting(self, ticker):
        try:
            tw = self.pq_loc_dir + f"{ticker}_TW.parquet"
            df = pd.read_parquet(tw)
            df = df[df.index >= '2023-01-01']
        
        except:
            try:
                two = self.pq_loc_dir + f"{ticker}_TWO.parquet"
                df = pd.read_parquet(two)
                df = df[df.index >= '2023-01-01']

            except:
                print("no symbol existed")
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        df['ma'] = df['Close'].rolling(int(60)).mean()

        fig, ax = plt.subplots()
        fig.set_size_inches(8,4)
        ax.plot(df['ma'], label='ma60')
        ax.plot(df["Close"], label=ticker)
        ax.set_title(ticker)
        ax.legend()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0)
    def insert_factor_tree(self):
        df = pd.DataFrame()
        df['A'] = [1, 2, 3]
        df['B'] = [1, 2, 3]
        df['C'] = [1, 2, 3]
        self.factor_dataframe.delete(*self.factor_dataframe.get_children())
        for i in range(len(df)):
            self.factor_dataframe.insert("", "end", values=(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2]))