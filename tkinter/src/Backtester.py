import customtkinter as ctk
import pandas as pd
from tkinter import ttk
class Backtester(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # params
        self.holding_period_dict = {
            '一週': 5,
            '兩週': 10,
            '一個月': 20, 
            '三個月': 60, 
            '六個月': 120
        }
        
        self.label_symbol = ctk.CTkLabel(self, text="策略名稱（自取）")
        self.label_symbol.grid(row=0, column=0, padx=10, pady=(5, 0))
        self.inputBox1 = ctk.CTkEntry(self, placeholder_text='策略名稱')
        self.inputBox1.grid(row=1, column=0, padx=10, pady=5)
 
        self.label_ma = ctk.CTkLabel(self, text="移動平均")
        self.label_ma.grid(row=0, column=1, padx=10, pady=(5, 0))
        self.menu_ma = ctk.CTkEntry(self, placeholder_text="20")
        self.menu_ma.grid(row=1, column=1, padx=10, pady=5)

        self.label_date = ctk.CTkLabel(self, text="持股期間（多久換一次股）")
        self.label_date.grid(row=0, column=2, padx=10, pady=(5, 0))
        self.menu_inputDate = ctk.CTkOptionMenu(self, values=['一週', '兩週', '一個月', '三個月', '六個月'])
        self.menu_inputDate.grid(row=1, column=2, padx=10, pady=5)

        self.inputButton1 = ctk.CTkButton(self, text='生成策略')
        self.inputButton1.grid(row=1, column=3, padx=10, pady=5)
        # Input Box and Buttons

    def search_stock_pq(self):
        stocks = self.input_stock.get()
        url = "../tw-stock-screener/database/0050_TW.parquet"
        df = pd.read_parquet(url)
        self.textbox.insert("end", stocks)
        self.textbox.insert("end", df)

    def delete_textbox(self):
        self.textbox.delete(0.0, "end")



        
