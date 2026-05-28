import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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


def register_student():
    print("\n===== Student Registration System =====")

    student_id = input(
        "Enter Student ID: "
    ).strip()

    student_name = input(
        "Enter Student Name: "
    ).strip()

    if not student_id or not student_name:
        print(
            "ID and Name cannot be empty!"
        )
        return

    folder_name = (
        f"{student_id}_{student_name}"
    )

    student_folder_path = os.path.join(
        DATASET_PATH,
        folder_name
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

        writer = csv.writer(file)

        
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

    print(
        "\n Student Registered Successfully!"
    )

    print(
        f" Folder Created:\n"
        f"{student_folder_path}"
    )


if __name__ == "__main__":
    register_student()