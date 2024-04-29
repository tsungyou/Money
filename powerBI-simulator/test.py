import tkinter as tk
from functions import get_stocks_from_json, read_json
import os
root = tk.Tk()
root.title('oxxo.studio')
root.geometry('1280x960')
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH)
stock_list = get_stocks_from_json()
# 定義 Label 顯示選取內容的函式
def show():
    n, = listbox.curselection()  # 取得項目索引值，因為是單選，回傳 (i,)，所以使用 n, 取值
    text.set(listbox.get(n))
    DIR_level2 = os.path.join(os.getcwd(), "level2")
    data = read_json(f"{DIR_level2}/{stock_list[n]}.json")
    level2_text.set(data['revenue'])
    print(data)  
    
def show_level3():
    n, = listbox.curselection()  # 取得項目索引值，因為是單選，回傳 (i,)，所以使用 n, 取值
    text.set(listbox.get(n))
    DIR_level3 = os.path.join(os.getcwd(), "level2")
    data = read_json(f"{DIR_level3}/{stock_list[n]}.json")
    level3_text.set(data['capex'])
    print(data)     # 設定文字變數內容為該索引值對應的內容

text = tk.StringVar()            # 設定文字變數
label = tk.Label(root, textvariable=text)  # 放入 Label
label.pack()

menu = tk.StringVar()
menu.set(stock_list)
left_frame = tk.Frame(main_frame, bg="light gray", width=100)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

listbox = tk.Listbox(left_frame,  listvariable=menu)
listbox.pack()

#  ============
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

level2_frame = tk.Frame(right_frame, bg="light blue", width=100)
level2_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
level2_text = tk.StringVar()
level2_label = tk.Label(level2_frame, textvariable=level2_text, bg="light blue")
level2_label.pack(expand=True, fill=tk.BOTH)

level3_frame = tk.Frame(right_frame, bg="light blue", width=100)
level3_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
level3_text = tk.StringVar()
level3_label = tk.Label(level3_frame, textvariable=level3_text, bg="black")
level3_label.pack(expand=True, fill=tk.BOTH)


#  btn left => level2=============
btn = tk.Button(left_frame, text='顯示', command=show)  # 放入 Button，設定 command 參數
btn.pack()

#  btn level2 => level3=============
btn = tk.Button(level2_frame, text='進階', command=show_level3)  # 放入 Button，設定 command 參數
btn.pack()


root.mainloop()