import cv2
import os
import csv
import pickle
import sqlite3
import face_recognition
import numpy as np
from datetime import datetime



BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "face_model.pkl"
)

ATTENDANCE_DIR = os.path.join(
    BASE_DIR,
    "attendence"
)

ATTENDANCE_FILE = os.path.join(
    ATTENDANCE_DIR,
    "attendence.csv"
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_FILE = os.path.join(
    DATABASE_DIR,
    "attendance.db"
)


def init_attendance_database():
    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    conn = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            UNIQUE(student_name, date)
        )
    """)

    if os.path.exists(
        ATTENDANCE_FILE
    ):
        with open(
            ATTENDANCE_FILE,
            "r"
        ) as file:
            reader = csv.reader(
                file
            )

            for row in reader:
                if (
                    len(row) < 3
                    or row[0] == "student_name"
                ):
                    continue

                cursor.execute(
                    """
                    INSERT OR IGNORE INTO attendance (
                        student_name,
                        date,
                        time
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        row[0],
                        row[1],
                        row[2]
                    )
                )

    conn.commit()
    conn.close()


def save_attendance_to_database(
    student_name,
    today_date,
    current_time
):
    init_attendance_database()

    conn = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO attendance (
            student_name,
            date,
            time
        )
        VALUES (?, ?, ?)
        """,
        (
            student_name,
            today_date,
            current_time
        )
    )

    inserted = (
        cursor.rowcount > 0
    )

    conn.commit()
    conn.close()

    return inserted



def mark_attendance(
    student_name
):

    today_date = datetime.now().strftime(
        "%d-%m-%Y"
    )

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    already_marked = False

  

    connection = sqlite3.connect(
        os.path.join(
            BASE_DIR,
            "database",
            "attendance.db"
        )
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM attendance
        WHERE student_name = ?
        AND date = ?
    """, (
        student_name,
        today_date
    ))

    existing_record = (
        cursor.fetchone()
    )

    if existing_record:
        already_marked = True

    

    if not already_marked:

        cursor.execute("""
            INSERT INTO attendance
            (
                student_name,
                date,
                time
            )
            VALUES (?, ?, ?)
        """, (
            student_name,
            today_date,
            current_time
        ))

        connection.commit()

    connection.close()

    

    file_exists = os.path.exists(
        ATTENDANCE_FILE
    )

    if not already_marked:

        with open(
            ATTENDANCE_FILE,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(
                file
            )

            if (
                not file_exists
                or
                os.path.getsize(
                    ATTENDANCE_FILE
                ) == 0
            ):
                writer.writerow([
                    "student_name",
                    "date",
                    "time"
                ])

            writer.writerow([
                student_name,
                today_date,
                current_time
            ])

        print(
            f" Attendance Marked: " 
            f"{student_name}"
        )



def recognize_faces():

    print(
        "\nLoading Model..."
    )

    init_attendance_database()

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        model_data = pickle.load(
            file
        )

    known_faces = (
        model_data[
            "encodings"
        ]
    )

    known_names = (
        model_data[
            "names"
        ]
    )

    camera = cv2.VideoCapture(0)

    print(
        "\nCamera Started"
    )

    while True:

        success, frame = (
            camera.read()
        )

        if not success:
            break

        small_frame = (
            cv2.resize(
                frame,
                (0, 0),
                fx=0.25,
                fy=0.25
            )
        )

        rgb_frame = (
            cv2.cvtColor(
                small_frame,
                cv2.COLOR_BGR2RGB
            )
        )

        face_locations = (
            face_recognition
            .face_locations(
                rgb_frame
            )
        )

        face_encodings = (
            face_recognition
            .face_encodings(
                rgb_frame,
                face_locations
            )
        )

        for (
            face_encoding,
            face_location
        ) in zip(
            face_encodings,
            face_locations
        ):

            matches = (
                face_recognition
                .compare_faces(
                    known_faces,
                    face_encoding,
                    tolerance=0.5
                )
            )

            name = (
                "Unknown Person"
            )

            confidence = 0

            face_distances = (
                face_recognition
                .face_distance(
                    known_faces,
                    face_encoding
                )
            )
            if len(
                face_distances
            ) > 0:

                best_match = np.argmin(
                    face_distances
                )

                if matches[
                    best_match
                ]:

                    full_name = (
                        known_names[
                            best_match
                        ]
                    )

                    name = (
                        full_name
                        .split("_", 1)[1]
                    )

                    confidence = (
                        round(
                            (
                                1
                                -
                                face_distances[
                                    best_match
                                ]
                            )
                            * 100,
                            2
                        )
                    )

                    mark_attendance(
                        full_name
                    )

            # Resize face box
            top, right, bottom, left = (
                face_location
            )

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Box Color
            color = (
                (0, 255, 0)
                if name !=
                "Unknown Person"
                else
                (0, 0, 255)
            )

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                color,
                2
            )

            label = (
                f"{name}"
            )

            if (
                name
                !=
                "Unknown Person"
            ):
                label += (
                    f" "
                    f"({confidence}%)"
                )

            cv2.putText(
                frame,
                label,
                (
                    left,
                    top - 10
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        cv2.imshow(
            "Smart Attendance System",
            frame
        )

        if (
            cv2.waitKey(1)
            & 0xFF
            == ord("q")
        ):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    recognize_faces()
