import cv2
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "student_images"
)

CAMERA_INDEX = 0
MAX_IMAGES = 50
WINDOW_NAME = "Face Capture"


def open_camera():
    backends = []

    if os.name == "nt":
        backends.extend([
            cv2.CAP_DSHOW,
            cv2.CAP_MSMF
        ])

    backends.append(None)

    for backend in backends:
        if backend is None:
            camera = cv2.VideoCapture(
                CAMERA_INDEX
            )
        else:
            camera = cv2.VideoCapture(
                CAMERA_INDEX,
                backend
            )

        if camera.isOpened():
            return camera

        camera.release()

    return None


def get_student_folder(
    student_id,
    student_name
):
    os.makedirs(
        DATASET_PATH,
        exist_ok=True
    )

    folder_name = (
        f"{student_id}_{student_name}"
    )

    folder_name_lower = folder_name.lower()

    for existing_folder in os.listdir(
        DATASET_PATH
    ):
        existing_path = os.path.join(
            DATASET_PATH,
            existing_folder
        )

        if (
            os.path.isdir(existing_path)
            and existing_folder.lower()
            == folder_name_lower
        ):
            return (
                existing_path,
                existing_folder
            )

    student_folder = os.path.join(
        DATASET_PATH,
        folder_name
    )

    os.makedirs(
        student_folder,
        exist_ok=True
    )

    print(
        f"Student folder created: "
        f"{student_folder}"
    )

    return (
        student_folder,
        folder_name
    )


def get_next_image_number(
    student_folder,
    folder_name
):
    max_number = 0

    for image_name in os.listdir(
        student_folder
    ):
        if not image_name.lower().endswith(
            ".jpg"
        ):
            continue

        prefix = (
            f"{folder_name}_"
        )

        if not image_name.startswith(
            prefix
        ):
            continue

        number_part = (
            image_name[
                len(prefix):-4
            ]
        )

        if number_part.isdigit():
            max_number = max(
                max_number,
                int(number_part)
            )

    return max_number + 1


def capture_faces():
    student_id = input(
        "Enter Student ID: "
    ).strip()

    student_name = input(
        "Enter Student Name: "
    ).strip()

    if (
        not student_id
        or not student_name
    ):
        print(
            "ID and Name cannot be empty!"
        )
        return

    student_folder, folder_name = (
        get_student_folder(
            student_id,
            student_name
        )
    )

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    if face_detector.empty():
        print(
            "Face detector not loaded"
        )
        return

    camera = open_camera()

    if camera is None:
        print(
            "Camera not available"
        )
        return

    next_image_number = get_next_image_number(
        student_folder,
        folder_name
    )

    captured_count = 0

    print(
        "\nCapturing face images..."
    )
    print(
        "Press q in the camera window to stop."
    )
    print(
        f"Saving to: {student_folder}"
    )

    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL
    )

    while captured_count < MAX_IMAGES:
        success, frame = camera.read()

        if not success:
            print(
                "Camera error"
            )
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (
            x,
            y,
            w,
            h
        ) in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            face_crop = frame[
                y:y + h,
                x:x + w
            ]

            image_path = os.path.join(
                student_folder,
                f"{folder_name}_"
                f"{next_image_number}.jpg"
            )

            if cv2.imwrite(
                image_path,
                face_crop
            ):
                captured_count += 1
                next_image_number += 1
            else:
                print(
                    f"Could not save image: "
                    f"{image_path}"
                )

            if captured_count >= MAX_IMAGES:
                break

        cv2.putText(
            frame,
            f"Captured: {captured_count}/{MAX_IMAGES}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            WINDOW_NAME,
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

    print(
        f"\n{captured_count} face images captured!"
    )


if __name__ == "__main__":
    capture_faces()
