import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import subprocess

from register_student import (
    register_student
)

from capture_faces import (
    capture_faces
)


# ----------------------------
# Register Student Window
# ----------------------------

def open_register_window():

    register_window = tk.Toplevel(
        root
    )

    register_window.title(
        "Register Student"
    )

    register_window.geometry(
        "400x250"
    )

    register_window.resizable(
        False,
        False
    )

    title_label = tk.Label(
        register_window,
        text="Register Student",
        font=(
            "Arial",
            16,
            "bold"
        )
    )

    title_label.pack(
        pady=15
    )

    tk.Label(
        register_window,
        text="Student Name",
        font=("Arial", 12)
    ).pack(
        pady=5
    )

    student_name_entry = tk.Entry(
        register_window,
        width=30,
        font=("Arial", 12)
    )

    student_name_entry.pack(
        pady=5
    )

    # ----------------------------
    # Save Student
    # ----------------------------

    def save_student():

        student_name = (
            student_name_entry
            .get()
            .strip()
        )

        if not student_name:

            messagebox.showerror(
                "Error",
                "Student name is required!"
            )

            return

        try:

            student_id, _ = (
                register_student(
                    student_name
                )
            )

            messagebox.showinfo(
                "Info",
                (
                    f"Student Registered\n\n"
                    f"ID: {student_id}\n"
                    f"Name: {student_name}\n\n"
                    f"Starting face capture..."
                )
            )

            # # Auto Face Capture
            # capture_faces(
            #     student_id,
            #     student_name
            # )

            # messagebox.showinfo(
            #     "Success",
            #     "Face Capture Completed!"
            # )
            
            # ----------------------------
            # Capture Faces
            # ----------------------------

            capture_faces(
                student_id,
                student_name
            )

            messagebox.showinfo(
                "Info",
                "Face Capture Completed!\n\n"
                "Training Model..."
            )

            # ----------------------------
            # Auto Train Model
            # ----------------------------

            subprocess.run([
                "py",
                "-3.11",
                "train_model.py"
            ])

            messagebox.showinfo(
                "Success",
                (
                    "Student Registered Successfully!\n\n"
                    "Face Captured\n"
                    "Model Trained\n"
                    "System Ready"
                )
            )
            
            
            register_window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    register_btn = tk.Button(
        register_window,
        text="Register & Capture Face",
        command=save_student,
        width=25,
        height=2
    )

    register_btn.pack(
        pady=20
    )


# ----------------------------
# Train Model
# ----------------------------

def train_model():

    try:

        subprocess.run([
            "py",
            "-3.11",
            "train_model.py"
        ])

        messagebox.showinfo(
            "Success",
            "Model Training Completed!"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ----------------------------
# Start Attendance
# ----------------------------

def start_attendance():

    try:

        subprocess.run([
            "py",
            "-3.11",
            "mark_attendance.py"
        ])

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ----------------------------
# View Attendance
# ----------------------------

def view_attendance():

    window = tk.Toplevel(
        root
    )

    window.title(
        "Attendance Records"
    )

    window.geometry(
        "700x400"
    )

    columns = (
        "ID",
        "Student Name",
        "Date",
        "Time"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for col in columns:

        table.heading(
            col,
            text=col
        )

        table.column(
            col,
            width=150
        )

    table.pack(
        fill="both",
        expand=True
    )

    # ----------------------------
    # Fetch Attendance
    # ----------------------------

    connection = sqlite3.connect(
        "database/attendance.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM attendance
    """)

    records = (
        cursor.fetchall()
    )

    for row in records:

        table.insert(
            "",
            tk.END,
            values=row
        )

    connection.close()


# ----------------------------
# Exit System
# ----------------------------

def exit_system():

    root.destroy()


# ----------------------------
# Main Window
# ----------------------------

root = tk.Tk()

root.title(
    "Smart Attendance System"
)

root.geometry(
    "500x550"
)

root.resizable(
    False,
    False
)


# ----------------------------
# Title
# ----------------------------

title_label = tk.Label(
    root,
    text=(
        "Smart Attendance\n"
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


# ----------------------------
# Buttons
# ----------------------------

btn_width = 25
btn_height = 2


register_btn = tk.Button(
    root,
    text="Register Student",
    width=btn_width,
    height=btn_height,
    command=open_register_window
)

register_btn.pack(
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


view_btn = tk.Button(
    root,
    text="View Attendance",
    width=btn_width,
    height=btn_height,
    command=view_attendance
)

view_btn.pack(
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


# ----------------------------
# Run App
# ----------------------------

root.mainloop()