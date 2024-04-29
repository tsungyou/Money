import tkinter as tk
from functions import get_stocks_from_json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
# built-in package

def draw_default(event):
    plt.close()
    x = [event]*5
    y = [5, 4, 3, 2, 1]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Sample Graph')

    # Create a canvas to display the graph
    canvas = FigureCanvasTkAgg(fig, master=level2_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False)


def on_button_click(event):
    selected_index = button_listbox.curselection()
    if selected_index:
        # Clear the contents of level2_frame
        for widget in level2_frame.winfo_children():
            widget.destroy()
        
        # Get the selected button data
        button_index = selected_index[0]
        button_text = buttons_data[button_index]
        show_value(button_text)
        
        # Draw the new graph in level2_frame
        draw_default(event)
def show_value(value):
    # Example: Display the value in a label
    value_label.config(text=f"Selected value: {value}")
def show_level2_tag(value):
    level2_text.set(value)
    show_value(value)
# Initialize Tkinter
root = tk.Tk()
root.title("Basic PowerBI GUI")

main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH)

# =========================== Left part (Search bar or navigator)
left_frame = tk.Frame(main_frame, bg="light gray", width=100)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

button_listbox = tk.Listbox(left_frame, yscrollcommand=scrollbar.set)
button_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
buttons_data = get_stocks_from_json("list_of_stocks.json")
button_listbox.config(width=max([len(i) for i in buttons_data]))
scrollbar.config(command=button_listbox.yview)


level2_text = tk.StringVar()
level3_text = tk.StringVar()

i = 1

# Labels to display data in level2 and level3
value_label = tk.Label(root, text="")
value_label.pack()
for button_data in buttons_data:
    button_listbox.insert(i, button_data)
    # Use lambda function with default argument to capture the value of button_data
    button_listbox.bind("<Button-1>", show_level2_tag(button_data)) # print(button_listbox)
    # button_listbox.bind(f"<Button-1>", on_button_click)
    i += 1
# ===========================
# Right part with two halves (level2 and level3)
frame_width = 200
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

level2_frame = tk.Frame(right_frame, bg="light blue", width=frame_width)
level2_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
level2_label = tk.Label(level2_frame, textvariable=level2_text, bg="light blue")
level2_label.pack(expand=True, fill=tk.BOTH)

# Right part - lower half (level3)
level3_frame = tk.Frame(right_frame, bg="light green", width=frame_width)
level3_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)





show_graph_button = tk.Button(root, text="Show Graph", command=draw_default)
show_graph_button.pack()
# Binding level2 click event
# Run the main event loop
root.mainloop()
