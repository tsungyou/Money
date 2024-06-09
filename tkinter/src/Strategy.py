import customtkinter as ctk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import json

class Strategy(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.factor_table   = pd.read_csv("database/factors/factors_table.csv")
        self.canvas         = None
        self.close          = pd.read_parquet('database/Adj_close.parquet')
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
        self.factor_dataframe = ttk.Treeview(self, columns=("策略名稱", "總報酬", "Sharpe", "年化報酬", "最大回檔"), show="headings", style="Treeview")
        self.factor_dataframe.heading("策略名稱", text="策略名稱")
        self.factor_dataframe.heading("總報酬", text="總報酬")
        self.factor_dataframe.heading("Sharpe", text="Sharpe")
        self.factor_dataframe.heading("年化報酬", text="年化報酬")
        self.factor_dataframe.heading("最大回檔", text="最大回檔")
        self.factor_dataframe.bind("<ButtonRelease-1>", self.on_factor_click)
        self.factor_dataframe.grid(row=0, column=0, padx=2, pady=2, sticky='n')
        self.insert_factor_tree()

        self.factor_selection_dataframe = ttk.Treeview(self, columns=("股票代號", "選入日期", "自選入起報酬"), show="headings", style="Treeview")
        self.factor_selection_dataframe.heading("股票代號", text="股票代號")
        self.factor_selection_dataframe.heading("選入日期", text="選入日期")
        self.factor_selection_dataframe.heading("自選入起報酬", text="自選入起報酬")
        self.factor_selection_dataframe.bind("<ButtonRelease-1>", self.on_tree_click)
        self.factor_selection_dataframe.grid(row=0, column=1, padx=2, pady=2, sticky='n')

        self.plotting(2330)

        self.textbox = ctk.CTkTextbox(self, width=200, height=200, corner_radius=20)
        self.textbox.grid(row=1, column=1, padx=2, pady=2, sticky='nsew')
        self.textbox.insert("end", f"=========================策略描述=========================\n")
    
    def on_factor_click(self, event):
        self.insert_factor_tree()


        item = self.factor_dataframe.identify('item', event.x, event.y)
        factor_name = self.factor_dataframe.item(item, "values")[0]
        # action 1
        with open("database/factors/factor_description.json", "r") as f:
            data = json.load(f)
        self.textbox.delete("1.0", 'end')
        self.textbox.insert("end", f"=========================策略描述=========================\n")
        self.textbox.insert("end", f"========================={factor_name}=========================\n")
        self.textbox.insert('end', data[factor_name] + '\n')
        # action 2
        
        df = pd.read_csv(f"database/factors/{factor_name}.csv")
        self.factor_selection_dataframe.delete(*self.factor_selection_dataframe.get_children())
        for i in range(len(df)):
            self.factor_selection_dataframe.insert("", "end", values=(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2]))
    def on_tree_click(self, event):
        item = self.factor_selection_dataframe.identify('item', event.x, event.y)
        symbol = self.factor_selection_dataframe.item(item, "values")[0]
        self.symbol = symbol
        self.plotting(self.symbol.split(".")[0])
    def plotting(self, ticker):
        try:
            df = self.close[ticker + ".TW"]
        except:
            try:
                df = self.close[ticker + ".TWO"]
            except:
                print("no symbol existed")
                return
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        ma = df.rolling(int(60)).mean()

        fig, ax = plt.subplots()
        fig.set_size_inches(8,4)
        ax.plot(ma, label='ma60')
        ax.plot(df, label=ticker)
        ax.set_title(ticker)
        ax.legend()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0)
    def insert_factor_tree(self):
        self.factor_table = pd.read_csv("database/factors/factors_table.csv")
        
        self.factor_dataframe.delete(*self.factor_dataframe.get_children())
        for i in range(len(self.factor_table)):
            self.factor_dataframe.insert("", "end", values=(self.factor_table.iloc[i, 0], self.factor_table.iloc[i, 1], self.factor_table.iloc[i, 2], self.factor_table.iloc[i, 3], self.factor_table.iloc[i, 4]))