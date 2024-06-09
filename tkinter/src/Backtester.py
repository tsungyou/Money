import customtkinter as ctk
import pandas as pd
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

class Backtester(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = None
        self.factor_description_loc = "database/factors/factor_description.json"
        self.close  = pd.read_parquet('database/Adj_close.parquet')
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
        self.label_name = ctk.CTkLabel(self, text="策略名稱（自取）")
        self.label_name.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.input_name = ctk.CTkEntry(self, placeholder_text='策略名稱')
        self.input_name.grid(row=1, column=i, padx=10, pady=5)

        i += 1

        self.label_da_start = ctk.CTkLabel(self, text='回測起始日')
        self.label_da_start.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.menu_da_start  = ctk.CTkOptionMenu(self, values=[str(i) for i in range(2013, 2021)])
        self.menu_da_start.grid(row=1, column=i, padx=10, pady=5)
        
        i += 1

        self.label_ma = ctk.CTkLabel(self, text="移動平均")
        self.label_ma.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.menu_ma = ctk.CTkEntry(self, placeholder_text="20")
        self.menu_ma.grid(row=1, column=i, padx=10, pady=5)

        i += 1

        self.label_holding_period = ctk.CTkLabel(self, text="持股期間（多久換一次股）")
        self.label_holding_period.grid(row=0, column=i, padx=10, pady=(5, 0))
        self.menu_holding_period = ctk.CTkOptionMenu(self, values=['一週', '兩週', '一個月', '三個月', '六個月'])
        self.menu_holding_period.grid(row=1, column=i, padx=10, pady=5)

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
        self.textbox_action = ctk.CTkTextbox(self, width=400, height=400, corner_radius=20)
        self.textbox_action.grid(row=1, column=i, padx=2, pady=2, sticky='nsew')
        self.textbox_action.insert("end", self.explanation_text)
    
        i += 1

    def generate_strategy(self):
        name = self.input_name.get()

        pool = self.input_pool.get()
        holding_period = self.menu_holding_period.get()
        holding = self.holding_period_dict[holding_period]

        # input error handling
        if name == "":
            name = f'unnamed, {str(np.random.random_integers(0, 10000))}'
        self.textbox_action.delete("1.0", 'end')
        self.textbox_action.insert("end", "請選擇移動平均週期, 持股期間並點擊生成策略\n")

        # backtest material
        weighting  = self.get_weighting()
        pct_change = self.get_pct_change(weighting, lag=1)

        # rigorous one
        rigoruous_backtest = self.backtest(weighting, pct_change)

        # basic backtest
        cumsum     = self.get_cumsum(weighting, pct_change)
        mdd = 0
        sharpe = 0
        total_return = 0
        annual_return = 0
        self.textbox_action.insert("end", f"""
        ========回測結果(完全不考慮手續費, 換手率的結果, 實際效果仍須至前頁確認)========\n
        sharpe        : {sharpe} \n
        total_return  : {total_return} \n
        annual_return : {annual_return} \n
        max drawdown  : {mdd} \n
        """)
        self.write_into_factors_table_csv(name, total_return, sharpe, annual_return, mdd)
        self.write_into_factor_description_json(name, description=f"移動平均選股")
        self.write_new_csv_holdings()

        self.plotting(cumsum)

    def get_weighting(self):
        da_start = self.menu_da_start.get()
        ma = self.menu_ma.get()
        df = self.close[self.close.index >= f'{da_start}-01-01']
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

    def get_pct_change(self, weighting, lag=1):
        pct_change = self.close[self.close.index >= weighting.index[0]].pct_change(fill_method=None)
        pct_change_lag1 = pct_change.shift(-1+lag)
        return pct_change_lag1
    
    def backtest(self, weighting, pct_change):
        pass

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
    
    def write_into_factors_table_csv(self, name, total_return, sharpe, cagr, mdd):
        file_loc = 'database/factors/factors_table.csv'
        df = pd.read_csv(file_loc, index_col=0).T
        df[name] = [total_return, sharpe, cagr, mdd]
        df.T.to_csv(file_loc)
        return None
    
    def write_into_factor_description_json(self, name, description):
        try:
            with open(self.factor_description_loc, "r") as f:
                data = json.load(f)
            data[name] = description
            with open(self.factor_description_loc, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except:
            print("fail writing into factor_descroption.json")
            return False
    
    def write_new_csv_holdings(self):
        pass

    def plotting(self, nav):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        fig, ax = plt.subplots()
        fig.set_size_inches(16, 8)
        ax.plot(nav, label='nav plot')
        ax.legend()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=0, pady=5)
