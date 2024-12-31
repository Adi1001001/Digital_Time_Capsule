import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageFont
from tkinter import font
from datetime import datetime

# standards
dark_grey = '#1b1c18'
white_text = '#eef2df'
# colour set
sky_blue = '#90AFC5'
deep_rust = '#763626'
dark_charcoal = '#2A3132'
Camelia_Path = "C:\\Users\\Adi\\Coding\\zfonts_RNS_Camelia.ttf"
Camelia = ImageFont.truetype(Camelia_Path, size = 16)

# window configuration
window = ttk.Window(themename = 'journal')
window.title('Digital Time Capsule')
window.geometry('1000x800')
window.resizable(True, True) # allowing the window to be resizable
window.configure(bg = dark_charcoal)

# main stuff
print('the window is on right now')
title_text = ttk.Label(master = window, text = 'The Digital Time Capsule', font = ("Times New Roman", 24, "bold"), background = dark_charcoal, foreground = sky_blue)
title_text.pack(pady = 25)

memory_input = tk.Text(master = window, background = sky_blue)
memory_input.pack()

def create_new_memory():
    date = str(datetime.today())
    date, date_time = date.split(' ')
    date_hour, date_minute = date_time.split(':')[:2]
    final_hour = int(date_hour)
    date_minute = int(date_minute)
    if date_minute >= 30:
        final_hour += 1
    final_year, final_month, final_day = date.split('-')
    final_year = int(final_year)
    final_month = int(final_month)
    final_day = int(final_day)
    total_days = 0
    #amount of days
    if final_month > 1:
        total_days += 31
        if final_month > 2:
            total_days += 28
            if final_month > 2:
                if final_month > 3:
                    total_days += 31
                    if final_month > 4:
                        total_days += 30
                        if final_month > 5:
                            total_days += 31
                            if final_month > 6:
                                total_days += 30
                                if final_month > 7:
                                    total_days += 31
                                    if final_month > 8:
                                        total_days += 31
                                        if final_month > 9:
                                            total_days += 30
                                            if final_month > 10:
                                                total_days += 31
                                                if final_month > 11:
                                                    total_days += 30
                                                    total_days += final_day
                                                else:
                                                    total_days += final_day
                                            else:
                                                total_days += final_day
                                        else:
                                            total_days += final_day
                                    else:
                                        total_days += final_day
                                else:
                                    total_days += final_day
                            else:
                                total_days += final_day
                        else:
                            total_days += final_day
                    else:
                        total_days += final_day
                else:
                    total_days += final_day
            else:
                total_days += final_day
        else:
            total_days += final_day
    else:
        total_days += final_day
    print(total_days)

new_memory_button = tk.Button(window, text = "Create a new memory", command = create_new_memory, font = ("Times New Roman", 12), foreground = deep_rust)
new_memory_button.pack(pady = 20)
    
window.mainloop()

# after window is closed
print('the window has closed')
