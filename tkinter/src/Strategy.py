import customtkinter as ctk
class Strategy(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to the Stock Info Page")
        label.pack(pady=20)