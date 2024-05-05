import tkinter as tk
from tkinter import ttk
import json

def get_collections_by_colname(colname):
    with open(cols_list_file, "r") as f:
        data = json.load(f)
    matching_strings = [item for item in data if colname in item]
    sub_dict = {key: data[key] for key in matching_strings if key in data}
    return sub_dict

def search(event=None):
    tree.delete(*tree.get_children())  # Clear previous search results
    colname = entry.get()
    result = get_collections_by_colname(colname)
    for key, value in result.items():
        database, collection = value.split("/")
        tree.insert("", "end", values=(key, database, collection))

# Path to the file containing collections list
cols_list_file = "cols_list.json"

# Create the main window
root = tk.Tk()
root.title("Search Collections by Column Name")

# Set the size of the main window
root.geometry("800x600")

# Create a label and an entry for user input
label = tk.Label(root, text="Enter column name:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

# Bind the Return key to the search function
entry.bind("<Return>", search)

# Create a button to trigger the search
button = tk.Button(root, text="Search", command=search)
button.pack()

# Create a Treeview widget to display the result
tree = ttk.Treeview(root, columns=("Key", "Database", "Collection"), show="headings")
tree.heading("Key", text="Key")
tree.heading("Database", text="Database")
tree.heading("Collection", text="Collection")
tree.pack()

# Run the main event loop
root.mainloop()
