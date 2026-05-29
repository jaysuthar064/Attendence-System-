import os
import sqlite3
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from capture_faces import capture_faces
from mark_attendence import init_attendance_database
from mark_attendence import recognize_faces
from register_student import register_student
from train_model import train_model as train_face_model


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_FILE = os.path.join(
    BASE_DIR,
    "database",
    "attendance.db"
)


def run_in_background(
    task,
    success_message=None,
    after_success=None
):
    set_status(
        "Working..."
    )

    def worker():
        try:
            task()

        except Exception as error:
            root.after(
                0,
                lambda: show_error(error)
            )
            return

        root.after(
            0,
            lambda: task_finished(
                success_message,
                after_success
            )
        )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


def task_finished(
    success_message,
    after_success
):
    set_status(
        "Ready"
    )

    if success_message:
        messagebox.showinfo(
            "Success",
            success_message
        )

    if after_success:
        after_success()


def show_error(
    error
):
    set_status(
        "Error"
    )

    messagebox.showerror(
        "Error",
        str(error)
    )


def set_status(
    text
):
    status_var.set(
        text
    )


def open_register_window():
    register_window = tk.Toplevel(
        root
    )

    register_window.title(
        "Register Student"
    )

    register_window.geometry(
        "420x330"
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
        text="Student ID",
        font=("Arial", 12)
    ).pack(
        pady=5
    )

    student_id_entry = tk.Entry(
        register_window,
        width=30,
        font=("Arial", 12)
    )

    student_id_entry.pack(
        pady=5
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

    def save_student():
        student_id = (
            student_id_entry
            .get()
            .strip()
        )

        student_name = (
            student_name_entry
            .get()
            .strip()
        )

        if (
            not student_id
            or not student_name
        ):
            messagebox.showerror(
                "Error",
                "Student ID and name are required."
            )
            return

        register_window.destroy()

        def task():
            register_student(
                student_id,
                student_name
            )

            capture_faces(
                student_id,
                student_name
            )

            train_face_model()

        run_in_background(
            task,
            success_message=(
                "Student registered, face captured, "
                "and model trained."
            )
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


def train_model():
    run_in_background(
        train_face_model,
        success_message="Model Training Completed!"
    )


def start_attendance():
    run_in_background(
        recognize_faces,
        success_message="Attendance window closed."
    )


def ensure_attendance_table():
    init_attendance_database()


def view_attendance():
    ensure_attendance_table()

    window = tk.Toplevel(
        root
    )

    window.title(
        "Attendance Records"
    )

    window.geometry(
        "760x420"
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

    column_widths = {
        "ID": 80,
        "Student Name": 260,
        "Date": 180,
        "Time": 160
    }

    for col in columns:
        table.heading(
            col,
            text=col
        )

        table.column(
            col,
            width=column_widths[col],
            anchor="center"
        )

    table.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=12
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, student_name, date, time
        FROM attendance
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    for row in records:
        table.insert(
            "",
            tk.END,
            values=row
        )

    if not records:
        messagebox.showinfo(
            "Attendance Records",
            "No attendance records found."
        )


def exit_system():
    root.destroy()


root = tk.Tk()

root.title(
    "Smart Attendance System"
)

root.geometry(
    "500x590"
)

root.resizable(
    False,
    False
)


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


status_var = tk.StringVar(
    value="Ready"
)

status_label = tk.Label(
    root,
    textvariable=status_var,
    font=("Arial", 10)
)

status_label.pack(
    pady=5
)


root.mainloop()
