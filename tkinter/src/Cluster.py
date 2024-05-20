import customtkinter as ctk
class Cluster(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to the Portfolio Page")
        label.pack(pady=20)

        