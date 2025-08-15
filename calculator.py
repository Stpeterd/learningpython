# a calculator app in python

import tkinter

button_values = [
    ["AC", "+/-", "%", "÷"], 
    ["7", "8", "9", "×"], 
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]

row_count = len(button_values) #5
column_count = len(button_values[0]) #4

color_light_grey = "#D4D4D2"
color_black = "1c1c1c"
color_dark_grey = "#505050"
color_orange = "#FF9500"
color_white ="white"

#window setup
window = tkinter.Tk() #create new window
window.title("Calculator")
window.resizable(False, False)

frame = tkinter.frame(window)
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_black, foreground=color_white, anchor="e", width=column_count)
label.grid(row=0, column=0, columnspan=column_count, sticky="we")

for row in range(row_count):
    for column in range(column_count):
        value = button_values0[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial", 30), width=column_count-1, height=1, command=lambda value=value: button_clicked(value))
        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_grey)
        elif value in right_symbols:
                button.config(foregound=color_white, background=color_orange)
        else:
                button.config(foreground=color_white, background=color_dark_grey)

                button,grid(row=row+1, column=column)

frame.pack()
