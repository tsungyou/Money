import customtkinter as ctk
from tkinter import ttk
from tkinter import font
import requests
from bs4 import BeautifulSoup
import pandas as pd

class Cluster(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)

        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Configure buttons
        self.surge_button = ctk.CTkButton(self, text='漲幅排行', command=self.insert_tree, width=100, height=50)
        self.surge_button.grid(row=0, column=0, padx=2, pady=2, sticky='n')

        self.down_button = ctk.CTkButton(self, text='跌幅排行', command=self.insert_tree1, width=100, height=50)
        self.down_button.grid(row=0, column=1, padx=2, pady=2, sticky='n')

        # Configure treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 20))
        style.configure("Treeview", rowheight=50, font=("Helvetica", 20))

        self.tree = ttk.Treeview(self, columns=("Symbol", "Price", "Percentage"), show="headings", style="Treeview")
        self.tree.heading("Symbol", text="Symbol")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Percentage", text="Percentage")
        self.tree.grid(row=1, column=0, padx=2, pady=2, sticky='nsew')

        self.tree1 = ttk.Treeview(self, columns=("Symbol", "Price", "Percentage"), show="headings", style="Treeview")
        self.tree1.heading("Symbol", text="Symbol")
        self.tree1.heading("Price", text="Price")
        self.tree1.heading("Percentage", text="Percentage")
        self.tree1.grid(row=1, column=1, padx=2, pady=2, sticky='nsew')

        self.pack(expand=True, fill='both')


    def insert_tree(self):
        df = self.get_surge()
        self.tree.delete(*self.tree.get_children())
        for i in range(len(df)):
            self.tree.insert("", "end", values=(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 3]))
    def get_surge(self):
            # 目标URL
        url = 'https://tw.stock.yahoo.com/rank/change-up'

        # 发送请求获取网页内容
        response = requests.get(url)
        if response.status_code != 200:
            print('Failed to retrieve data')
            exit()

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        s = soup.find_all("div", {"class": "Pos(r) Ov(h)"})
        s1 = soup.find_all("li", class_="List(n)")
        #df = pd.DataFrame()
        data = []
        for i in s1:
            s = str(i).split(">")
            indices = [14, 17, 24, 30, 36, 40, 44, 48, 56]

            # 提取指定索引的元素
            try:
                col1 = [s[k] for k in indices]
            except IndexError as e:
                print(f"IndexError: {e} - Some indices are out of range for the split list.")

            col1 = [q.split("<")[0] for q in col1]
            data.append(col1[1:])
            #df[col1[0]] = col1[1:]
            # 打印结果

        #df_close = df.T
        header = ['股號', '股價', '漲跌', '漲跌幅(%)','最高','最低','價差', '成交金額(億)']
        #df_close.columns = ['股號', '股價', '漲跌', '漲跌幅(%)','最高','最低','價差', '成交金額(億)']
        df = pd.DataFrame(data, columns=header)
        numeric_columns = ['股價', '漲跌', '最高','最低','價差', '成交金額(億)']
        for column in numeric_columns:
            df[column] = df[column].str.replace(',', '')
        return df

    def insert_tree1(self):
        df = self.get_down()
        self.tree1.delete(*self.tree1.get_children())
        for i in range(len(df)):
            self.tree1.insert("", "end", values=(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 3]))
    def get_down(self):
            # 目标URL
        url = 'https://tw.stock.yahoo.com/rank/change-down'

        # 发送请求获取网页内容
        response = requests.get(url)
        if response.status_code != 200:
            print('Failed to retrieve data')

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        s = soup.find_all("div", {"class": "Pos(r) Ov(h)"})
        s1 = soup.find_all("li", class_="List(n)")
        #df = pd.DataFrame()
        data = []
        for i in s1:
            s = str(i).split(">")
            indices = [14, 17, 24, 30, 36, 40, 44, 48, 56]

            # 提取指定索引的元素
            try:
                col1 = [s[k] for k in indices]
            except IndexError as e:
                print(f"IndexError: {e} - Some indices are out of range for the split list.")

            col1 = [q.split("<")[0] for q in col1]
            data.append(col1[1:])
            #df[col1[0]] = col1[1:]
            # 打印结果

        #df_close = df.T
        header = ['股號', '股價', '漲跌', '漲跌幅(%)','最高','最低','價差', '成交金額(億)']
        #df_close.columns = ['股號', '股價', '漲跌', '漲跌幅(%)','最高','最低','價差', '成交金額(億)']
        df = pd.DataFrame(data, columns=header)
        numeric_columns = ['股價', '漲跌', '最高','最低','價差', '成交金額(億)']
        for column in numeric_columns:
            df[column] = df[column].str.replace(',', '')
        return df