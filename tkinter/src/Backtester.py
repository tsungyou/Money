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

        self.inputButton1 = ctk.CTkButton(self, text='生成策略', command=self.generate_strategy)
        self.inputButton1.grid(row=1, column=3, padx=10, pady=5)

        self.label_pool = ctk.CTkLabel(self, text='股池篩選(top)')
        self.label_pool.grid(row=0, column=4, padx=10, pady=(5, 0))
        self.input_pool = ctk.CTkEntry(self, placeholder_text='500')
        self.input_pool.grid(row=1, column=4, padx=10, pady=5)
        # Input Box and Buttons
        self.label_action = ctk.CTkLabel(self, text="Action")
        self.label_action.grid(row=0, column=5, padx=10, pady=(5, 0))
        self.textbox_action = ctk.CTkTextbox(self, width=200, height=200, corner_radius=20)
        self.textbox_action.grid(row=1, column=5, padx=2, pady=2, sticky='nsew')
        self.textbox_action.insert("end", "請選擇移動平均週期, 持股期間並點擊生成策略\n")
    
    def generate_strategy(self):
        ma   = self.menu_ma.get()
        pool = self.input_pool.get()

        holding_period = self.menu_inputDate.get()
        holding_period_dict = {
            "一週": 5,
            '兩週': 10,
            '一個月': 20,
            '三個月': 60,
            '六個月': 120
        }
        holding = holding_period_dict[holding_period]
        self.textbox_action.delete("1.0", 'end')
        self.textbox_action.insert("end", "請選擇移動平均週期, 持股期間並點擊生成策略\n")
        self.textbox_action.insert("end", holding)
        
        close  = pd.read_parquet('database/Adj_close.parquet')
        volume = pd.read_parquet('database/Volume.parquet')
        # run backtest
        
        