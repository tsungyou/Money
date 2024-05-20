import customtkinter as ctk
class Screener(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to the Settings Page")
        label.pack(pady=20)