# Import the required modules
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from subprocess import call

# Create a Tkinter window
window = tk.Tk()
window.title("Insert Image with ID")
window.geometry("400x200+550+150")

# Define some padding values for the widgets
padx = 10
pady = 5

# Create a label for the title of the form
title_label = tk.Label(window, text="Insert Image with ID", font=("Arial", 16))
title_label.pack(padx=padx, pady=pady)

# Create a frame to hold the entry widgets and labels
frame = tk.Frame(window)
frame.pack(padx=padx, pady=pady)

# Create labels and entry widgets for each field
id_label = tk.Label(frame, text="ID:")
id_entry = tk.Entry(frame)
id_label.grid(row=0, column=0, sticky=tk.E)
id_entry.grid(row=0, column=1)

# Define a function to open the file dialog and get the path of the selected image
def open_file_dialog():
    path = filedialog.askopenfilename(title="Select an Image")
    return path

def call_EncodeGenerator():
    call(["python","EncodeGenerator.py"])

# Define a function to insert the image with ID in the desired folder and change the name of the image with ID as a name
def insert_image():
    # Get the values from the entry widgets
    id_val = id_entry.get()

    # Open the file dialog to select an image
    path = open_file_dialog()

    # Open the selected image using PIL
    img = Image.open(path)

    # Get the directory where the script is located
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create a new directory if it doesn't exist already
    if not os.path.exists(dir_path + "/image"):
        os.makedirs(dir_path + "/image")

    # Save the image in the images directory with ID as a name in png format
    img.save(dir_path + "/image/" + id_val + ".png")

    # Show a message box to indicate that image was inserted successfully
    tk.messagebox.showinfo("Success", "Image inserted successfully!")
    call_EncodeGenerator()
    window.destroy()

# Create a button to insert the image with ID in the desired folder and change the name of the image with ID as a name
insert_button = tk.Button(window, text="Insert Image", command=insert_image)
insert_button.pack(padx=padx, pady=pady)

# Run the Tkinter event loop
window.mainloop()


