"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import io
import csv
import firebase_admin
from firebase_admin import credentials, firestore


class State(rx.State):
    show_menu: bool = False
    upload_message: str = ""

    def toggle_menu(self):
        self.show_menu = not self.show_menu

    def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            self.upload_message = "❌ No file selected. Please select a CSV file to upload."
            return
        file = files[0]
        try:
            content = file.file.read()
            csvfile = io.StringIO(content.decode("utf-8"))
            reader = csv.DictReader(csvfile)
            required_columns = {"id", "first_name", "last_name", "subj_1", "subj_2"}
            if not required_columns.issubset(set(reader.fieldnames or [])):
                self.upload_message = "❌ CSV missing required columns: id, first_name, last_name, subj_1, subj_2."
                return
            count = self.upload_csv_to_firebase(reader)
            self.upload_message = f"✅ Uploaded {count} students from {file.filename} successfully!"
        except Exception as e:
            self.upload_message = f"❌ Error: {e}"

    def upload_csv_to_firebase(self, reader) -> int:
        if not firebase_admin._apps:
            cred = credentials.Certificate(
                "api-keys/api-keysmegamot-402d2-firebase-adminsdk-fbsvc-61c10d0de0.json"
            )
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        count = 0
        for row in reader:
            doc_id = row.get('id')
            if doc_id:
                db.collection('students').document(doc_id).set(row)
                count += 1
        return count


def admin_menu():
    return rx.box(
        rx.button("admin", color="blue", on_click=State.toggle_menu),
        rx.cond(
            State.show_menu,
            rx.box(
                rx.upload(
                    rx.button("upload csv", size="1", variant="ghost", width="6em", height="2em", font_size="0.8em", padding="0.2em 0.5em"),
                    accept=".csv",
                    max_files=1,
                    on_upload=State.handle_upload
                ),
                rx.text(State.upload_message, color="red", margin_top="0.5em"),
                box_shadow="md",
                border="1px solid #e2e8f0",
                border_radius="md",
                bg="white",
                padding="0.5em",
                margin_top="0.5em"
            )
        ),
        width="fit-content",
        margin="1em"
    )


def index():
    return rx.center(
        rx.vstack(
            admin_menu(),
            spacing="4",
            padding="2em"
        ),
        min_height="100vh"
    )


app = rx.App()
app.add_page(index)
