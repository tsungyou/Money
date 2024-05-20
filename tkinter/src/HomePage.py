import customtkinter as ctk
from tkinter import ttk
class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=("Key", "Database", "Collection"), show="headings")
        self.tree.heading("Key", text="Key")
        self.tree.heading("Database", text="Database")
        self.tree.heading("Collection", text="Collection")
        self.tree.pack(pady=80)
