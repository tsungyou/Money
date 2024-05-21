import customtkinter as ctk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Strategy(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = None
        self.pq_loc_dir = "../tw-stock-screener/database/"

        self.inputBox1 = ctk.CTkEntry(self, placeholder_text='Stock symbol')
        self.inputBox1.pack(padx=10, pady=10)

        self.inputButton1 = ctk.CTkButton(self, text='Show Plot', command=self.plotting)
        self.inputButton1.pack(padx=30, pady=10)
        self.inputButton1.bind("<Return>", self.plotting)
        # generate the figure and plot object which will be linked to the root elemen

        # initiate the window

    def plotting(self):
        ticker = self.inputBox1.get()
        
        try:
            tw = self.pq_loc_dir + f"{ticker}_TW.parquet"
            df = pd.read_parquet(tw)
        except:
            try:
                two = self.pq_loc_dir + f"{ticker}_TWO.parquet"
                df = pd.read_parquet(two)
            except:
                print("no symbol existed")
        
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        fig, ax = plt.subplots()
        fig.set_size_inches(8,4)
        ax.plot(df["Close"])
        ax.axis("off")
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=0.15)