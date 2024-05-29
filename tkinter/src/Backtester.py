import customtkinter as ctk
import pandas as pd
from tkinter import ttk
class Backtester(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=("Date", "Open", "Close"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Open", text="Open")
        self.tree.heading("Close", text="Close")
        self.tree.pack(pady=40)

        self.label = ctk.CTkLabel(self, text="Welcome to the Settings Page")
        self.label.pack(pady=0)

        self.input_stock = ctk.CTkEntry(self, placeholder_text='20')
        self.input_stock.pack(pady=10)

        self.button_stock = ctk.CTkButton(self, text='Search Stock', command=self.search_stock_pq)
        self.button_stock.pack(pady=20)

        self.button_delete = ctk.CTkButton(self, text="Delete", command=self.delete_textbox)
        self.button_delete.pack(pady=30, padx=20)

        self.textbox = ctk.CTkTextbox(self)
        self.textbox.pack(pady=40)

    def search_stock_pq(self):
        stocks = self.input_stock.get()
        url = "../tw-stock-screener/database/0050_TW.parquet"
        df = pd.read_parquet(url)
        self.textbox.insert("end", stocks)
        self.textbox.insert("end", df)

    def delete_textbox(self):
        self.textbox.delete(0.0, "end")



        
