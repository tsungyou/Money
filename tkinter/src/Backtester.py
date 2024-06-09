import customtkinter as ctk
import pandas as pd
from tkinter import ttk
import numpy as np

class Backtester(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.explanation_text = """
        請選擇移動平均週期, 持股期間並點擊生成策略\n
        例：選擇ma = 20: \n
        1. 以20天ma和股價的差分(diff)為因子的值 \n
        2. 對於選擇的股池依照因子大小分配權重(因子的值為正且越大=>分配越高權重) \n
        3. 顯示的圖會是不含手續費, 每天根據算出的權重調整(檢測因子有效性) \n
        """
        # params
        self.holding_period_dict = {
            '一週': 5,
            '兩週': 10,
            '一個月': 20, 
            '三個月': 60, 
            '六個月': 120
        }
        i = 0
        self.label_symbol = ctk.CTkLabel(self, text="策略名稱（自取）")
        self.label_symbol.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.inputBox1 = ctk.CTkEntry(self, placeholder_text='策略名稱')
        self.inputBox1.grid(row=1, column=i, padx=10, pady=5)

        i += 1

        self.label_date = ctk.CTkLabel(self, text='回測起始日')
        self.label_date.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.menu_da_start  = ctk.CTkOptionMenu(self, values=[str(i) for i in range(2013, 2021)])
        self.menu_da_start.grid(row=1, column=i, padx=10, pady=5)
        
        i += 1

        self.label_ma = ctk.CTkLabel(self, text="移動平均")
        self.label_ma.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.menu_ma = ctk.CTkEntry(self, placeholder_text="20")
        self.menu_ma.grid(row=1, column=i, padx=10, pady=5)

        i += 1

        self.label_date = ctk.CTkLabel(self, text="持股期間（多久換一次股）")
        self.label_date.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.menu_inputDate = ctk.CTkOptionMenu(self, values=['一週', '兩週', '一個月', '三個月', '六個月'])
        self.menu_inputDate.grid(row=1, column=i, padx=10, pady=5)

        i += 1

        self.label_pool = ctk.CTkLabel(self, text='股池篩選(top)')
        self.label_pool.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.input_pool = ctk.CTkEntry(self, placeholder_text='500')
        self.input_pool.grid(row=1, column=i, padx=10, pady=5)

        i += 1

        self.inputButton1 = ctk.CTkButton(self, text='生成策略', command=self.generate_strategy)
        self.inputButton1.grid(row=1, column=i, padx=10, pady=5)

        i += 1

        # Input Box and Buttons
        self.label_action = ctk.CTkLabel(self, text="Action")
        self.label_action.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.textbox_action = ctk.CTkTextbox(self, width=400, height=200, corner_radius=20)
        self.textbox_action.grid(row=1, column=i, padx=2, pady=2, sticky='nsew')
        self.textbox_action.insert("end", self.explanation_text)
    
        i += 1

    def generate_strategy(self):
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

        close  = pd.read_parquet('database/Adj_close.parquet')
        
        weighting  = self.get_weighting(close)
        pct_change = self.get_pct_change(close, weighting, lag=1)
        cumsum     = self.get_cumsum(weighting, pct_change)
        mdd = 0
        sharpe = 0
        total_return = 0
        annual_return = 0
        self.textbox_action.insert("end", f"""
        ============回測結果============\n
        sharpe        : {sharpe} \n
        total_return  : {total_return} \n
        annual_return : {annual_return} \n
        max drawdown  : {mdd} \n
        """)
        print(cumsum)

    def get_weighting(self, close):
        da_start = self.menu_da_start.get()
        ma = self.menu_ma.get()
        df = close[close.index >= f'{da_start}-01-01']
        df = df.dropna(how='all', axis=1)
        df = df.dropna(how='all', axis=0)

        ma20 = df.rolling(window=int(ma)).mean()
        diff_ma20 = df/ma20 - 1
        diff_ma20.dropna(how='all', axis=0, inplace=True)
        diff_ma20
        # def get_demean_weighting(self, data):
        df1 = diff_ma20.dropna(axis='columns', how='all').copy()
        demean = df1.sub(df1.mean(axis=1), axis=0)
        weighting = demean.div(demean.abs().sum(axis=1), axis=0)
        return weighting

    def get_pct_change(self, close, weighting, lag=1):
        pct_change = close[close.index >= weighting.index[0]].pct_change(fill_method=None)
        pct_change_lag1 = pct_change.shift(-1+lag)
        return pct_change_lag1

    def get_cumsum(self, weighting, pct_change_shift1):

        pct_change_shift1.dropna(how='all', axis=0, inplace=True)
        weighting_da = weighting[weighting.index >= pct_change_shift1.index[0]]
        nav_df = (weighting_da * pct_change_shift1)
        nav = nav_df.sum(axis=1)
        
        # remove abnormal returns
        average = np.mean(nav)
        std = np.std(nav)
        nav.loc[nav[nav > average + 3*std].index] = 0
        cumsum = nav.cumsum()
        return cumsum
        
        