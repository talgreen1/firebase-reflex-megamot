"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx


class State(rx.State):
    show_menu: bool = False

    def toggle_menu(self):
        self.show_menu = not self.show_menu


def admin_menu():
    return rx.box(
        rx.button("admin", color="blue", on_click=State.toggle_menu),
        rx.cond(
            State.show_menu,
            rx.box(
                rx.button("upload csv", size="2", variant="ghost"),
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
