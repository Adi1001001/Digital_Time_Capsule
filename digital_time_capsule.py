import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageFont
from tkinter import font

# standards
dark_grey = '#1b1c18'
white_text = '#eef2df'
Camelia_Path = "C:\\Users\\Adi\\Coding\\zfonts_RNS_Camelia.ttf"
Camelia = ImageFont.truetype(Camelia_Path, size = 16)

# window configuration
window = ttk.Window(themename = 'journal')
window.title('Digital Time Capsule')
window.geometry('600x400')
window.resizable(True, True) # allowing the window to be resizable
window.configure(bg = dark_grey)

# main stuff
print('the window is on right now')
title_text = ttk.Label(master = window, text = 'The Digital Time Capsule', font = ("Times New Roman", 24, "bold"), background = dark_grey, foreground = white_text)
title_text.pack(pady = 25)

window.mainloop()

# after window is closed
print('the window has closed')