"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import firebase_admin
from firebase_admin import credentials, firestore
import os

from rxconfig import config


# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(
        os.path.join("api-keys", "api-keysmegamot-402d2-firebase-adminsdk-fbsvc-61c10d0de0.json")
    )
    firebase_admin.initialize_app(cred)
db = firestore.client()


class State(rx.State):
    """The app state."""

    student_id: str = ""
    subj_1: str = ""
    subj_2: str = ""
    error: str = ""

    def set_student_id(self, value: str):
        self.student_id = value
        self.error = ""
        self.subj_1 = ""
        self.subj_2 = ""

    def fetch_subjects(self):
        self.error = ""
        self.subj_1 = ""
        self.subj_2 = ""
        if not self.student_id:
            self.error = "נא להזין תעודת זהות."
            return
        try:
            doc_ref = db.collection("Students").document(self.student_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                self.subj_1 = data.get("subj_1", "")
                self.subj_2 = data.get("subj_2", "")
                if not self.subj_1 and not self.subj_2:
                    self.error = "לא נמצאו מקצועות לתלמיד."
            else:
                self.error = "תלמיד/ה לא נמצא/ה."
        except Exception as e:
            self.error = f"שגיאה: {e}"

    def on_key_down(self, e):
        # Reflex passes the event as a string (the key pressed), not a dict
        if e == "Enter":
            self.fetch_subjects()


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
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


def student_subjects() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.text("תעודת זהות התלמיד/ה", size="5", font_weight="bold"),
            rx.input(
                placeholder="הכנס/י תעודת זהות...",
                value=State.student_id,
                on_change=State.set_student_id,
                on_blur=State.set_student_id,
                on_key_down=State.on_key_down,  # Use on_key_down instead of on_submit
                width="300px",
                dir="rtl",
            ),
            rx.button("חפש", on_click=State.fetch_subjects, width="100px"),
            rx.cond(State.error != "", rx.text(State.error, color="red")),
            rx.cond(
                (State.subj_1 != ""),
                rx.text("מקצוע 1: " + State.subj_1, size="4", color="green"),
            ),
            rx.cond(
                (State.subj_2 != ""),
                rx.text("מקצוע 2: " + State.subj_2, size="4", color="green"),
            ),
            spacing="4",
            align_items="center",
            min_height="60vh",
        ),
    )


app = rx.App()
app.add_page(student_subjects, route="/")
