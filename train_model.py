import os
import cv2
import pickle
import face_recognition


# Base Path
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "student_images"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "face_model.pkl"
)


def train_model():

    known_faces = []
    known_names = []

    print("\n Training Started...\n")

    # Loop through students
    for student_folder in os.listdir(
        DATASET_PATH
    ):

        student_path = os.path.join(
            DATASET_PATH,
            student_folder
        )

        # Skip files
        if not os.path.isdir(
            student_path
        ):
            continue

        student_name = (
            student_folder
        )

        print(
            f"Processing: "
            f"{student_name}"
        )

        # Loop images
        for image_name in os.listdir(
            student_path
        ):

            image_path = os.path.join(
                student_path,
                image_name
            )

            try:
                image = cv2.imread(
                    image_path
                )

                rgb_image = (
                    cv2.cvtColor(
                        image,
                        cv2.COLOR_BGR2RGB
                    )
                )

                # Face encoding
                face_encodings = (
                    face_recognition
                    .face_encodings(
                        rgb_image
                    )
                )

                if (
                    len(
                        face_encodings
                    ) > 0
                ):
                    known_faces.append(
                        face_encodings[0]
                    )

                    known_names.append(
                        student_name
                    )

            except Exception as e:
                print(
                    f"Error: "
                    f"{image_name}"
                )

    # Save model
    model_data = {
        "encodings":
        known_faces,

        "names":
        known_names
    }

    with open(
        MODEL_PATH,
        "wb"
    ) as file:

        pickle.dump(
            model_data,
            file
        )

    print(
        "\n Training Complete!"
    )

    print(
        f"Total Faces Trained: "
        f"{len(known_names)}"
    )


if __name__ == "__main__":
    train_model()