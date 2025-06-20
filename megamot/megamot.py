"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import csv
import firebase_admin
from firebase_admin import credentials, firestore
import os
import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""
    upload_message: str = ""
    upload_files: list[rx.UploadFile] = []

    def on_file_upload(self, files: list[rx.UploadFile]):
        self.upload_files = files
        self.upload_message = f"Selected {files[0].filename}" if files else "No file selected."

    def handle_upload(self):
        csv_path = os.path.join("csvs", "UUStudents.csv")
        if not os.path.exists(csv_path):
            self.upload_message = "csvs/UUStudents.csv not found. Please upload the file manually."
            return
        try:
            count = self.upload_csv_to_firebase(csv_path)
            self.upload_message = f"Uploaded {count} students from UUStudents.csv successfully!"
        except Exception as e:
            self.upload_message = f"Error: {e}"

    def upload_csv_to_firebase(self, csv_path: str) -> int:
        # Initialize Firebase if not already
        if not firebase_admin._apps:
            cred = credentials.Certificate("api-keys/api-keysmegamot-402d2-firebase-adminsdk-fbsvc-61c10d0de0.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        count = 0
        with open(csv_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            if 'id' not in reader.fieldnames:
                raise ValueError("CSV missing 'id' column header.")
            for row in reader:
                doc_id = row.get('id')
                if doc_id:
                    db.collection('students').document(doc_id).set(row)
                    count += 1
        if count == 0:
            raise ValueError("No students found in CSV or 'id' column is empty.")
        return count


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            rx.divider(),
            rx.heading("Upload Student List CSV", size="7"),
            rx.upload(
                accept=".csv",
                multiple=False
            ),
            rx.text("After selecting a file, please place it in the 'csvs' folder and click the button below."),
            rx.button("Upload csvs/UUStudents.csv to Firebase", on_click=State.handle_upload),
            rx.text(State.upload_message, color="green"),
            spacing="5",
            justify_content="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


app = rx.App()
app.add_page(index)
