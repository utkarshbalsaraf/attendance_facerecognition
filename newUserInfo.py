# Import the required modules
import tkinter as tk
import firebase_admin
from firebase_admin import credentials, db
from tkinter import messagebox
from datetime import datetime
from subprocess import call

# creating and connecting the database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "enter your"
})

ref = db.reference('Students')

# Create a Tkinter window
window = tk.Tk()
window.title("Registration Form")
window.geometry("400x400+550+150")

# Define some padding values for the widgets
padx = 10
pady = 5

# Create a label for the title of the form
title_label = tk.Label(window, text="Registration Form", font=("Arial", 18))
title_label.pack(padx=padx, pady=pady)

# Create a frame to hold the entry widgets and labels
frame = tk.Frame(window)
frame.pack(padx=padx, pady=pady)

# Create labels and entry widgets for each field
id_label = tk.Label(frame, text="ID:")
id_entry = tk.Entry(frame)
id_label.grid(row=0, column=0, sticky=tk.E)
id_entry.grid(row=0, column=1,padx=padx,pady=pady)

name_label = tk.Label(frame, text="Full Name:")
name_entry = tk.Entry(frame)
name_label.grid(row=1, column=0, sticky=tk.E)
name_entry.grid(row=1, column=1,pady=pady)

course_label = tk.Label(frame, text="Course:")
course_entry = tk.Entry(frame)
course_label.grid(row=2, column=0, sticky=tk.E)
course_entry.grid(row=2, column=1,pady=pady)

year_label = tk.Label(frame, text="Starting Year:")
year_entry = tk.Entry(frame)
year_label.grid(row=3, column=0, sticky=tk.E)
year_entry.grid(row=3, column=1,pady=pady)

attendance_label = tk.Label(frame, text="Total Attendance:")
attendance_entry = tk.Entry(frame)
attendance_label.grid(row=4, column=0, sticky=tk.E)
attendance_entry.grid(row=4, column=1,pady=pady)

standing_label = tk.Label(frame, text="Standing:")
standing_entry = tk.Entry(frame)
standing_label.grid(row=5, column=0, sticky=tk.E)
standing_entry.grid(row=5, column=1,pady=pady)

grad_year_label = tk.Label(frame, text="Current Year of Graduation:")
grad_year_entry = tk.Entry(frame)
grad_year_label.grid(row=6, column=0, sticky=tk.E)
grad_year_entry.grid(row=6, column=1 ,pady=pady)

last_attendance_label = tk.Label(frame, text="Last Attendance Date:")
last_attendance_val = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
last_attendance_entry = tk.Entry(frame)
last_attendance_entry.insert(0,last_attendance_val)
last_attendance_entry.config(state='readonly')
last_attendance_label.grid(row=7, column=0, sticky=tk.E)
last_attendance_entry.grid(row=7, column=1, pady=pady)


def call_img_Insert():
    call(["python","image_insert.py"])

# Define a function to store the data to Firebase Realtime Database
def register():
    # Get the values from the entry widgets
    id_val = (id_entry.get())
    name_val = name_entry.get()
    course_val = course_entry.get()
    year_val = (year_entry.get()) # Convert to integer
    attendance_val = (attendance_entry.get()) # Convert to integer
    standing_val = standing_entry.get()
    grad_year_val = (grad_year_entry.get()) # Convert to integer
    last_attendance_val = last_attendance_entry.get()

    # Store the data to Firebase Realtime Database using the given data structure
    data = {
        id_val:
            {
                "name": name_val,
                "Course": course_val,
                "starting_year": int(year_val),
                "total_attendance": int(attendance_val),
                "standing": standing_val,
                "year": int(grad_year_val),
                "last_attendance_time": last_attendance_val
            }
    }

    ref.update(data)

    # Show a message box to indicate that registration was successful
    messagebox.showinfo("Success", "Registration successful!")
    window.destroy()
    call_img_Insert()

# Create a button to register the data
register_button = tk.Button(window, text="Register", command=register, width=15, font=3)
register_button.pack(padx=padx, pady=pady)

# Run the Tkinter event loop
window.mainloop()

