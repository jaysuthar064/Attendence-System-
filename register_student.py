import os
import csv
import sqlite3


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "student_images"
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "database",
    "students.csv"
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "attendance.db"
)


def ensure_student_table():
    os.makedirs(
        os.path.dirname(DB_PATH),
        exist_ok=True
    )

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            student_name TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def register_student(
    student_id,
    student_name
):
    if (
        not student_id
        or not student_name
    ):
        raise ValueError(
            "Student ID and name are required."
        )

    os.makedirs(
        DATASET_PATH,
        exist_ok=True
    )

    os.makedirs(
        os.path.dirname(CSV_FILE),
        exist_ok=True
    )

    ensure_student_table()

    folder_name = (
        f"{student_id}_{student_name}"
    )

    student_folder_path = (
        os.path.join(
            DATASET_PATH,
            folder_name
        )
    )

    os.makedirs(
        student_folder_path,
        exist_ok=True
    )

    file_exists = os.path.exists(
        CSV_FILE
    )

    student_exists_in_csv = False

    if file_exists:
        with open(
            CSV_FILE,
            mode="r",
            newline=""
        ) as file:
            reader = csv.reader(
                file
            )

            for row in reader:
                if (
                    len(row) >= 2
                    and row[0] == student_id
                ):
                    student_exists_in_csv = True
                    break

    if not student_exists_in_csv:
        with open(
            CSV_FILE,
            mode="a",
            newline=""
        ) as file:

            writer = csv.writer(
                file
            )

            if (
                not file_exists
                or
                os.path.getsize(
                    CSV_FILE
                ) == 0
            ):
                writer.writerow([
                    "student_id",
                    "student_name"
                ])

            writer.writerow([
                student_id,
                student_name
            ])

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO students (
            student_id,
            student_name
        )
        VALUES (?, ?)
        """,
        (
            student_id,
            student_name
        )
    )

    connection.commit()
    connection.close()

    return student_folder_path


if __name__ == "__main__":
    student_id_input = input(
        "Enter Student ID: "
    ).strip()

    student_name_input = input(
        "Enter Student Name: "
    ).strip()

    folder_path = register_student(
        student_id_input,
        student_name_input
    )

    print(
        "Student registered successfully."
    )

    print(
        f"Folder Created: {folder_path}"
    )
    
