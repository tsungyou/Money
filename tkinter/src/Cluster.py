import customtkinter as ctk
class Cluster(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to the Portfolio Page")
        label.pack(pady=20)

        input1 = ctk.CTkEntry(self, placeholder_text='20')
        input1.pack(pady=20)

