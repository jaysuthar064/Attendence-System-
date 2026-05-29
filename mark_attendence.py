import cv2
import os
import csv
import pickle
import face_recognition
from datetime import datetime


# Base Path
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


def mark_attendance(
    student_name
):
    os.makedirs(
        ATTENDANCE_DIR,
        exist_ok=True
    )

    today_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    already_marked = False

    # Create file if not exists
    file_exists = os.path.exists(
        ATTENDANCE_FILE
    )

    rows = []

    if file_exists:

        with open(
            ATTENDANCE_FILE,
            "r"
        ) as file:

            reader = csv.reader(file)

            rows = list(reader)

            for row in rows:

                if len(row) < 2:
                    continue

                if (
                    row[0] == student_name
                    and
                    row[1] == today_date
                ):
                    already_marked = True
                    break

    if not already_marked:

        with open(
            ATTENDANCE_FILE,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(
                file
            )

            # Header
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
            f"Attendance Marked: "
            f"{student_name}"
        )


def recognize_faces():

    print(
        "\nLoading Model..."
    )

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
        "\nCamera Started..."
    )

    while True:

        success, frame = (
            camera.read()
        )

        if not success:
            break

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
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
                    face_encoding
                )
            )

            name = "Unknown"

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

                best_match = (
                    face_distances
                    .argmin()
                )
                if matches[
                    best_match
                ]:
                    name = (
                        known_names[
                            best_match
                        ]
                    )

                    mark_attendance(
                        name
                    )

            top, right, bottom, left = (
                face_location
            )

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                name,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "Smart Attendance",
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
    
