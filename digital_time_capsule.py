import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageFont
from tkinter import messagebox
from datetime import datetime
from tkinter import Toplevel # for the notification
from database_handling import insert_memory, get_memories, delete_memories
# for attaining images
from tkinter import filedialog
from PIL import Image, ImageTk

# standards
dark_grey = '#1b1c18'
white_text = '#eef2df'
image_path = [] # file path to the images/files
image_there = False
image_counter = 0
recent_memories = []
big_memory_box = None
first = False
toggle_switch_on = True
# colour set
sky_blue = '#90AFC5'
deep_rust = '#763626'
dark_charcoal = '#2A3132'
Camelia_Path = "C:\\Users\\Adi\\Coding\\zfonts_RNS_Camelia.ttf"
Camelia = ImageFont.truetype(Camelia_Path, size = 16)

# window configuration
window = ttk.Window()
window.title('Digital Time Capsule')
# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight() - 100
window.geometry(f"{screen_width}x{screen_height}")
window.resizable(True, True) # allowing the window to be resizable

# icons
delete_button_image = Image.open("Digital Time Capsule/Assets/delete.png")
delete_button_image.thumbnail((50, 50))  # Resize for preview
delete_button_image_tk = ImageTk.PhotoImage(delete_button_image) # you have to convert into photoimage to display images in tkinter

on_button_image = Image.open("Digital Time Capsule/Assets/on-button.png")
on_button_image.thumbnail((50, 50))  # Resize for preview
on_button_image_tk = ImageTk.PhotoImage(on_button_image) # you have to convert into photoimage to display images in tkinter

off_button_image = Image.open("Digital Time Capsule/Assets/off-button.png")
off_button_image.thumbnail((50, 50))  # Resize for preview
off_button_image_tk = ImageTk.PhotoImage(off_button_image) # you have to convert into photoimage to display images in tkinter

# the different screens
frame0 = tk.Frame(window)
frame0.configure(bg = dark_charcoal)
frame1 = tk.Frame(window)
frame1.configure(bg = dark_charcoal)
frame2 = tk.Frame(window)
frame2.configure(bg = dark_charcoal)

navigation_frame0 = tk.Frame(frame0)
navigation_frame0.configure(bg = dark_charcoal)
navigation_frame1 = tk.Frame(frame1)
navigation_frame1.configure(bg = dark_charcoal)
navigation_frame2 = tk.Frame(frame2)
navigation_frame2.configure(bg = dark_charcoal)

# navigating between different windows/frames
def enter_home():
    frame0.tkraise()
    navigation_frame0.pack(side = "bottom")
    frame0.place(relwidth=1, relheight=1)
    clear_big_memory_box()
def enter_main_screen():
    global first
    frame1.tkraise()
    navigation_frame1.pack(side = "bottom")
    frame1.place(relwidth=1, relheight=1)
    if first:
        clear_big_memory_box()
    first = True
def enter_memory_log():
    navigation_frame2.pack(side = "bottom")
    recent_memories = get_memories()
    frame2.tkraise()
    frame2.place(relwidth=1, relheight=1)
    if recent_memories != None:
        create_table(recent_memories)
        window.after(100, update_scroll_region)  # Delay scroll region update by 100ms
    else:
        No_memories_button = ttk.Label(master = frame2, text = 'No memories created yet', font = ("Times New Roman", 24, "bold"), background = dark_charcoal, foreground = sky_blue)
        No_memories_button.pack(pady = 25)

home_button = tk.Button(navigation_frame0, text = "Enter home", font = ("Times New Roman", 16))
home_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')
home_button = tk.Button(navigation_frame1, text = "Enter home", font = ("Times New Roman", 16), command = enter_home)
home_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')
home_button = tk.Button(navigation_frame2, text = "Enter home", font = ("Times New Roman", 16), command = enter_home)
home_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')

main_screen_button = tk.Button(navigation_frame0, text = "Enter main screen", font = ("Times New Roman", 16), command = enter_main_screen)
main_screen_button.pack(pady=10, padx=150, ipadx = 20, side = 'left')
main_screen_button = tk.Button(navigation_frame1, text = "Enter main screen", font = ("Times New Roman", 16))
main_screen_button.pack(pady=10, padx=150, ipadx = 20, side = 'left')
main_screen_button = tk.Button(navigation_frame2, text = "Enter main screen", font = ("Times New Roman", 16), command = enter_main_screen)
main_screen_button.pack(pady=10, padx=150, ipadx = 20, side = 'left')

memory_log_button = tk.Button(navigation_frame0, text = "Enter memory log", font = ("Times New Roman", 16), command = enter_memory_log)
memory_log_button.pack(pady=10, padx=150, ipadx = 20, side = 'right')
memory_log_button = tk.Button(navigation_frame1, text = "Enter memory log", font = ("Times New Roman", 16), command = enter_memory_log)
memory_log_button.pack(pady=10, padx=150, ipadx = 20, side = 'right')
memory_log_button = tk.Button(navigation_frame2, text = "Enter memory log", font = ("Times New Roman", 16))
memory_log_button.pack(pady=10, padx=150, ipadx = 20, side = 'right')

# Create the canvas inside the frame
canvas = tk.Canvas(frame2, bg=dark_charcoal, width=screen_width, height=screen_height-200)
canvas.pack(side = "top", fill="both", expand=True)
# Add a vertical scrollbar to the canvas
scrollbar = ttk.Scrollbar(frame2, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# main stuff
title_text = ttk.Label(master = frame1, text = 'The Digital Time Capsule', font = ("Times New Roman", 24, "bold"), background = dark_charcoal, foreground = sky_blue)
title_text.pack(pady = 25)

memory_input = ttk.Text(master = frame1, background = sky_blue, width = 100, height = 15)
memory_input.pack(ipady=5)

thumbnail_box = ttk.Frame(frame1, width = 700, height = 150)
thumbnail_box.pack(pady=20)

# notifications
def show_notification_added_successfully():
    # Create a top-level window
    notification = Toplevel(frame1)
    
    # Set the window size and position
    notification.geometry(f"800x200+{int(screen_width/2-400)}+{int(screen_height/2-100)}")  # Width, Height, X, Y
    notification.resizable(False, False)
    
    # Remove the border and title bar for a "floating" effect
    notification.overrideredirect(True)
    
    # Add the message
    label = tk.Label(notification, text="Your memory has been saved!", font=("Arial", 24, "bold"))
    label.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Automatically close the notification after 2 seconds
    notification.after(2000, notification.destroy)
def show_notification_too_many_images():
    # Create a top-level window
    notification = Toplevel(frame1)
    
    # Set the window size and position
    notification.geometry(f"800x200+{int(screen_width/2-400)}+{int(screen_height/2-100)}")  # Width, Height, X, Y
    notification.resizable(False, False)
    
    # Remove the border and title bar for a "floating" effect
    notification.overrideredirect(True)
    
    # Add the message
    label = tk.Label(notification, text="Too many images!", font=("Arial", 24, "bold"))
    label.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Automatically close the notification after 2 seconds
    notification.after(2000, notification.destroy)
def show_memory_already_added():
    # Create a top-level window
    notification = Toplevel(frame1)
    
    # Set the window size and position
    notification.geometry(f"800x200+{int(screen_width/2-400)}+{int(screen_height/2-100)}")  # Width, Height, X, Y
    notification.resizable(False, False)
    
    # Remove the border and title bar for a "floating" effect
    notification.overrideredirect(True)
    
    # Add the message
    label = tk.Label(notification, text="Your memory has ALREADY been saved!", font=("Arial", 24, "bold"))
    label.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Automatically close the notification after 2 seconds
    notification.after(2000, notification.destroy)
def show_memory_deleted():
    # Create a top-level window
    notification = Toplevel(frame1)
    
    # Set the window size and position
    notification.geometry(f"800x200+{int(screen_width/2-400)}+{int(screen_height/2-100)}")  # Width, Height, X, Y
    notification.resizable(False, False)
    
    # Remove the border and title bar for a "floating" effect
    notification.overrideredirect(True)
    
    # Add the message
    label = tk.Label(notification, text="Your memory has been deleted!", font=("Arial", 24, "bold"))
    label.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Automatically close the notification after 2 seconds
    notification.after(2000, notification.destroy)
def show_confirmed_date():
    # Create a top-level window
    notification = Toplevel(frame1)
    
    # Set the window size and position
    notification.geometry(f"800x200+{int(screen_width/2-400)}+{int(screen_height/2-100)}")  # Width, Height, X, Y
    notification.resizable(False, False)
    
    # Remove the border and title bar for a "floating" effect
    notification.overrideredirect(True)
    
    # Add the message
    label = tk.Label(notification, text="You reminder date has been confirmed!", font=("Arial", 24, "bold"))
    label.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Automatically close the notification after 2 seconds
    notification.after(2000, notification.destroy)
def show_cofirmed_date_error():
    # Create a top-level window
    notification = Toplevel(frame1)
    
    # Set the window size and position
    notification.geometry(f"1000x200+{int(screen_width/2-500)}+{int(screen_height/2-100)}")  # Width, Height, X, Y
    notification.resizable(False, False)
    
    # Remove the border and title bar for a "floating" effect
    notification.overrideredirect(True)
    
    # Add the message
    label = tk.Label(notification, text="You have entered the reminder date incorrectly!", font=("Arial", 24, "bold"))
    label.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Automatically close the notification after 2 seconds
    notification.after(2000, notification.destroy)

toggle_switch_label = tk.Label(frame1, text = "Reminders are OFF", font = ("Times New Roman", 20), bg = dark_charcoal)
toggle_switch_label.place(x = 950, y = 775)
    

reminder_date_enter_label = tk.Label(frame1, text="Enter Date (DD/MM/YYYY) and hours (HH) (24 hour time):")
reminder_date_entry = ttk.Entry(frame1, width= 20)
reminder_hour_entry = ttk.Entry(frame1, width=10)

def validate_date():
    try:
        reminder_date = reminder_date_entry.get()
        reminder_hour = int(reminder_hour_entry.get())
        day, month, year = map(int, reminder_date.split('/'))
        if 1 <= day <= 31 and 1 <= month <= 12 and 0 <= reminder_hour <= 24:  # Basic validation
            current_date, current_time = str(datetime.today()).split(' ')
            current_year, current_month, current_day = current_date.split('-')
            current_hour, current_min = current_time.split(':')[:2]
            current_hour = int(current_hour)
            current_min = int(current_min)
            current_year = int(current_year)
            current_month = int(current_month)
            current_day = int(current_day)
            if current_min >= 30:
                current_hour += 1
            if year < current_year:
                raise ValueError
            elif year == current_year:
                if month < current_month:
                    raise ValueError
                elif month == current_month:
                    if day < current_day:
                        raise ValueError
                    elif day == current_day:
                        if reminder_hour <= current_hour:
                            raise ValueError
            show_confirmed_date()
            reminder_date_entry.delete(0, tk.END)
            reminder_hour_entry.delete(0, tk.END)
            return day, month, year, reminder_hour
        else:
            raise ValueError
    except ValueError:
        show_cofirmed_date_error()
        reminder_date_entry.delete(0, tk.END)
        reminder_hour_entry.delete(0, tk.END)

def toggle_switch():
    global toggle_switch_on

    if toggle_switch_on == True:
        set_reminder_button.config(image = on_button_image_tk)
        toggle_switch_label.config(text = "Reminders are ON", fg = "Green")

        reminder_date_enter_label.place(x = 500, y = 850)
        reminder_date_entry.place(x = 800, y = 850)
        reminder_hour_entry.place(x = 1000, y = 850)

        toggle_switch_on = False
    else:
        set_reminder_button.config(image = off_button_image_tk)
        toggle_switch_label.config(text = "Reminders are OFF", fg = "Red")

        reminder_date_entry.destroy()
        reminder_date_enter_label.destroy()
        reminder_hour_entry.destroy()

        toggle_switch_on = True

set_reminder_button = tk.Button(frame1, image = off_button_image_tk, command = toggle_switch, height = 45)
set_reminder_button.place(x = 850, y = 775)

def create_new_memory():
    global image_there, image_path, image_counter, reminder

    if toggle_switch_on == False:
        reminder_day, reminder_month, reminder_year, reminder_hour = validate_date()

    # get clean data on the memory text
    memory = memory_input.get("1.0", "end").strip()
    memory_input.delete("1.0", "end")

    # process the date and time
    date = str(datetime.today())
    date, date_time = date.split(' ')
    date_hour, date_minute = date_time.split(':')[:2] # split the date for the first 2 occurences that the : appears
    final_hour = int(date_hour)
    date_minute = int(date_minute)
    if date_minute >= 30:
        final_hour += 1
    final_year, final_month, final_day = date.split('-')
    final_year = int(final_year)
    final_month = int(final_month)
    final_day = int(final_day)

    #amount of days
    total_days = sum([
        31,  # January
        28,  # February (ignoring leap years for now)
        31,  # March
        30,  # April
        31,  # May
        30,  # June
        31,  # July
        31,  # August
        30,  # September
        31,  # October
        30,  # November
    ][:final_month - 1]) + final_day
    print(total_days, memory)

    # inserting the image path into the database
    if image_there and image_path != []:
        image_counter = 0
        if len(image_path) == 1:
            image_paths = image_path[0]
        else:
            image_paths = "|".join(image_path)
        if toggle_switch_on == True:
            error = insert_memory(memory, final_year, final_month, final_day, final_hour, image_paths)
        else:
            error = insert_memory(memory, final_year, final_month, final_day, final_hour, image_paths, reminder_year, reminder_month, reminder_day, reminder_hour)
    else:
        if toggle_switch_on == True:
            error = insert_memory(memory, final_year, final_month, final_day, final_hour)
        else: 
            error = insert_memory(memory, final_year, final_month, final_day, final_hour, reminder_year, reminder_month, reminder_day, reminder_hour)
    image_path = []
    image_there = False

    # Clear the thumbnails from the display
    for widget in thumbnail_box.winfo_children():
        widget.destroy()

    # show notification
    if error:
        show_memory_already_added()
    else:
        show_notification_added_successfully()

    toggle_switch()

new_memory_button = tk.Button(frame1, text = "Create a new memory", command = create_new_memory, font = ("Times New Roman", 16))
new_memory_button.pack(pady = 20)

# for desktop only
def show_image_preview(image_path):
    # Load and display the selected image as a thumbnail
    img = Image.open(image_path)
    img.thumbnail((150, 150))  # Resize for preview
    img_tk = ImageTk.PhotoImage(img) # you have to convert into photoimage to display images in tkinter
    # Add the thumbnail to the box
    label = tk.Label(thumbnail_box, image=img_tk, width = 150, height = 150)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.pack(side="left", padx=5)  # Adjust padding as needed

def get_images():
    global image_path, image_there, image_counter
    image_path.append(filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]))
    if image_path:
        image_counter += 1
        if image_counter > 4:
            del image_path[-1]
            show_notification_too_many_images()
        else:
            image_there = True
            show_image_preview(image_path[-1])
            print(image_path)

emoji_button = tk.Button(frame1, text="📸", font = ("Times New Roman", 16), command = get_images)
emoji_button.pack()

# Enable mouse wheel scrolling
def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Update the scrollregion whenever the scrollable frame changes size
def update_scroll_region():
    canvas.configure(scrollregion=canvas.bbox("all"))

def delete_table_entry(id):
    delete_memories(id)
    show_memory_deleted()
    clear_big_memory_box()
    recent_memories = get_memories()
    create_table(recent_memories)

def create_table(memories):
    global big_memory_box, screen_height, screen_width

    big_memory_box = ttk.Frame(canvas, width = screen_width, height = screen_height)
    canvas.create_window((0, 0), window=big_memory_box, anchor="nw")  # Add big_memory_box to the canvas

    # Configure column weights for resizing
    big_memory_box.grid_columnconfigure(0, weight=1, minsize=30)  # ID column, smaller size
    big_memory_box.grid_columnconfigure(1, weight=3, minsize=900)  # Memory Text column, larger size
    big_memory_box.grid_columnconfigure(2, weight=1, minsize=250)  # Date column, smaller size
    big_memory_box.grid_columnconfigure(3, weight=2, minsize=1000)  # Images column, larger size
    big_memory_box.grid_columnconfigure(3, weight=1, minsize=100)  # Delete column, smaller size

    # Creating table headers
    headers = ['ID', 'Memory Text', 'Date', 'Images', 'Delete']

    # Adding headers to the first row
    for col, header in enumerate(headers): # enumerate allows you to use the for loop normally and keep track of the index for each element
        header_label = tk.Label(big_memory_box, text=header, font=("Arial", 12, "bold"), anchor = "center")
        header_label.grid(row=1, column=col, padx=10, pady=5)

    # ADDING THE ACTUAL ROWS

    # Iterate through the database results and populate rows
    for i, memory in enumerate(memories):
        id, memory_text, year, month, day, hour, image_path = memory
        
        # Displaying the ID, memory text, and formatted date
        date_str = f"{day}/{month}/{year} {hour}:00"
        row_data = [id, memory_text, date_str]

        for j, data in enumerate(row_data):
            data_label = tk.Label(big_memory_box, text=data, font=("Arial", 12))
            data_label.grid(row=i + 2, column=j, padx=10, pady=5)

        # Adding the images
        if image_path == None:
            image_box = tk.Label(big_memory_box, text = "No images", font=("Arial", 12))
            image_box.grid(row=i + 2, column=3, padx=10, pady=5)
        else:
            if '|' in image_path: # more than 1 image
                # Create a frame for image navigation
                img_frame = tk.Frame(big_memory_box)
                img_frame.grid(row=i + 2, column=3, padx=10, pady=5)

                image_paths = image_path.split('|')
                for idx, image in enumerate(image_paths):
                    img = Image.open(image)
                    img.thumbnail((100, 100))  # Resize for preview
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(img_frame, image=img_tk)
                    img_label.image = img_tk  # Keep a reference to avoid garbage collection
                    img_label.grid(row=0, column=idx, padx=10, pady=5)
            else: # 1 image
                img = Image.open(image_path)
                img.thumbnail((200, 150))  # Resize for preview
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(big_memory_box, image=img_tk)
                img_label.image = img_tk  # Keep a reference to avoid garbage collection
                img_label.grid(row=i + 2, column=3, padx=10, pady=5)
        
        # adding the delete button
        delete_button = tk.Button(big_memory_box, image=delete_button_image_tk, command=lambda x=id: delete_table_entry(x)) # the lambda somehow gets the value of the id from when the button was created and when it is clicked it outputs it
        delete_button.grid(row=i + 2, column=4, padx=10, pady=5)
        delete_button.image = delete_button_image_tk

    update_scroll_region()

# FRAME 2

def clear_big_memory_box():
    global big_memory_box
    big_memory_box.destroy()

# FRAME 0

enter_main_screen()
window.mainloop()

# after window is closed
