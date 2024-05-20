import customtkinter as ctk
class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to the Home Page")
        label.pack(pady=20)