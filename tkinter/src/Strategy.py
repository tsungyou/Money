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
        item = self.factor_dataframe.identify('item', event.x, event.y)
        factor_name = self.factor_dataframe.item(item, "values")[0]
        # action 1
        with open("src/factor_description.json", "r") as f:
            data = json.load(f)
        self.textbox.delete("1.0", 'end')
        self.textbox.insert("end", f"=========================策略描述=========================\n")
        self.textbox.insert("end", f"========================={factor_name}=========================\n")
        self.textbox.insert('end', data[factor_name] + '\n')
        # action 2
        
        df = pd.read_csv(f"src/{factor_name}.csv")
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
        df = pd.read_csv("src/factors_table.csv")
        
        self.factor_dataframe.delete(*self.factor_dataframe.get_children())
        for i in range(len(df)):
            self.factor_dataframe.insert("", "end", values=(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3], df.iloc[i, 4]))