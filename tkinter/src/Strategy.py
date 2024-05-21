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

        # generate the figure and plot object which will be linked to the root elemen

        self.stratMenu = ctk.CTkOptionMenu(self, values=['strat1', "strat2", 'strat3'], command=self.get_strat_result)
        self.stratMenu.pack()
        # initiate the window

    def get_strat_result(self):
        strat = self.stratMenu.get()
        