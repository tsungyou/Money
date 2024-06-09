import customtkinter as ctk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Searcher(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = None

        self.close  = pd.read_parquet('database/Adj_close.parquet')

        # Labels for each input
        self.label_symbol = ctk.CTkLabel(self, text="股票代號")
        self.label_symbol.grid(row=0, column=0, padx=10, pady=(5, 0))
        self.inputBox1 = ctk.CTkEntry(self, placeholder_text='2330')
        self.inputBox1.grid(row=1, column=0, padx=10, pady=5)

        self.label_ma = ctk.CTkLabel(self, text="移動平均")
        self.label_ma.grid(row=0, column=1, padx=10, pady=(5, 0))
        self.menu_ma = ctk.CTkOptionMenu(self, values=["20", "60", "120", "100"], command=self.plotting)
        self.menu_ma.grid(row=1, column=1, padx=10, pady=5)

        self.label_date = ctk.CTkLabel(self, text="開始年度")
        self.label_date.grid(row=0, column=2, padx=10, pady=(5, 0))
        self.menu_inputDate = ctk.CTkOptionMenu(self, values=['2019', '2020', '2021', '2022', '2023', '2024'], command=self.plotting)
        self.menu_inputDate.grid(row=1, column=2, padx=10, pady=5)

        self.inputButton1 = ctk.CTkButton(self, text='顯示', command=self.plotting)
        self.inputButton1.grid(row=1, column=3, padx=10, pady=5)

        # default plot
        self.plotting()

    def plotting(self):
        # set ticker default
        ma = self.menu_ma.get()
        ticker = self.inputBox1.get()
        date = self.menu_inputDate.get()
        if ticker == "":
            ticker = "2330"

        # set ma default
        try:
            df = self.close[ticker + ".TW"]
            df = df[df.index >= f'{date}-01-01']
        except:
            try:
                df = self.close[ticker + ".TWO"]
                df = df[df.index >= f'{date}-01-01']
            except:
                print("no symbol existed")
                return
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        ma = df.rolling(int(ma)).mean()

        fig, ax = plt.subplots()
        fig.set_size_inches(16, 8)
        ax.plot(ma, label='ma')
        ax.plot(df, label='close')
        ax.set_title(ticker)
        ax.legend()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=5, pady=10)
