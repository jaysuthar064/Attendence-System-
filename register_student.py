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


def register_student(
    student_id,
    student_name
):

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

    cursor.execute("""
        INSERT INTO students
        (
            student_id,
            student_name
        )
        VALUES (?, ?)
    """, (
        student_id,
        student_name
    ))

    connection.commit()
    connection.close()

    return student_folder_path