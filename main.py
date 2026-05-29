import os
import sqlite3
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_FILE = os.path.join(
    BASE_DIR,
    "database",
    "attendance.db"
)

VENV_PYTHON = os.path.join(
    BASE_DIR,
    ".venv",
    "Scripts",
    "python.exe"
)

PYTHON_EXE = (
    VENV_PYTHON
    if os.path.exists(VENV_PYTHON)
    else sys.executable
)


def run_script(
    script_name,
    wait=False,
    success_message=None
):
    script_path = os.path.join(
        BASE_DIR,
        script_name
    )

    if not os.path.exists(
        script_path
    ):
        messagebox.showerror(
            "Missing File",
            f"Cannot find {script_name}"
        )
        return

    command = [
        PYTHON_EXE,
        script_path
    ]

    creation_flags = 0

    if os.name == "nt":
        creation_flags = (
            subprocess.CREATE_NEW_CONSOLE
        )

    try:
        if wait:
            result = subprocess.run(
                command,
                cwd=BASE_DIR,
                creationflags=creation_flags
            )

            if result.returncode != 0:
                messagebox.showerror(
                    "Script Error",
                    (
                        f"{script_name} exited with "
                        f"code {result.returncode}"
                    )
                )
                return

            if success_message:
                messagebox.showinfo(
                    "Success",
                    success_message
                )
        else:
            subprocess.Popen(
                command,
                cwd=BASE_DIR,
                creationflags=creation_flags
            )

    except Exception as error:
        messagebox.showerror(
            "Script Error",
            str(error)
        )


def ensure_attendance_table():
    os.makedirs(
        os.path.dirname(DATABASE_FILE),
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            UNIQUE(student_name, date)
        )
    """)

    connection.commit()
    connection.close()


def register_student():
    run_script(
        "register_student.py"
    )


def capture_faces():
    run_script(
        "capture_faces.py"
    )


def train_model():
    run_script(
        "train_model.py",
        wait=True,
        success_message="Model Training Completed!"
    )


def start_attendance():
    run_script(
        "mark_attendence.py"
    )


def view_attendance():
    ensure_attendance_table()

    window = tk.Toplevel(root)

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
    "AI Smart Attendance System"
)

root.geometry(
    "500x580"
)

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


root.mainloop()
