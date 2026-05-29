import tkinter as tk
from tkinter import messagebox
import subprocess




def register_student():

    subprocess.run([
        "py",
        "-3.11",
        "register_student.py"
    ])


def capture_faces():

    subprocess.run([
        "py",
        "-3.11",
        "capture_faces.py"
    ])


def train_model():

    subprocess.run([
        "py",
        "-3.11",
        "train_model.py"
    ])

    messagebox.showinfo(
        "Success",
        "Model Training Completed!"
    )


def start_attendance():

    subprocess.run([
        "py",
        "-3.11",
        "mark_attendance.py"
    ])


def exit_system():

    root.destroy()




root = tk.Tk()

root.title(
    "AI Smart Attendance System"
)

root.geometry("500x500")

root.resizable(
    False,
    False
)




title_label = tk.Label(
    root,
    text=(
        "AI Smart Attendance\n"
        "System"
    ),
    font=(
        "Arial",
        20,
        "bold"
    )
)

title_label.pack(
    pady=20
)




btn_width = 25
btn_height = 2


register_btn = tk.Button(
    root,
    text="Register Student",
    width=btn_width,
    height=btn_height,
    command=register_student
)

register_btn.pack(
    pady=10
)


capture_btn = tk.Button(
    root,
    text="Capture Faces",
    width=btn_width,
    height=btn_height,
    command=capture_faces
)

capture_btn.pack(
    pady=10
)


train_btn = tk.Button(
    root,
    text="Train Model",
    width=btn_width,
    height=btn_height,
    command=train_model
)

train_btn.pack(
    pady=10
)


attendance_btn = tk.Button(
    root,
    text="Start Attendance",
    width=btn_width,
    height=btn_height,
    command=start_attendance
)

attendance_btn.pack(
    pady=10
)


exit_btn = tk.Button(
    root,
    text="Exit",
    width=btn_width,
    height=btn_height,
    command=exit_system
)

exit_btn.pack(
    pady=20
)




root.mainloop()