import flet as ft


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name, self.text, self.message_type = user_name, text, message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__(
            vertical_alignment="start",
            controls=[
                ft.CircleAvatar(content=ft.Text(message.user_name[:1].capitalize()),
                                color=ft.colors.WHITE,
                                bgcolor=self.get_avatar_color(message.user_name)),
                ft.Column([ft.Text(message.user_name, weight="bold"),
                           ft.Text(message.text, selectable=True)],
                          tight=True, spacing=5),
            ]
        )

    @staticmethod
    def get_avatar_color(user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):
    page.horizontal_alignment, page.title = "stretch", "Flet Chat"

    def join_chat_click(e):
        if not join_username.value:
            join_username.error_text, join_username.update = "Name cannot be blank!", True
        else:
            page.session.set("user_name", join_username.value)
            page.dialog.open, new_message.prefix = False, ft.Text(
                f"{join_username.value}: ")
            page.pubsub.send_all(Message(user_name=join_username.value,
                                         text=f"{join_username.value} has joined the chat.",
                                         message_type="login_message"))
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(page.session.get(
                "user_name"), new_message.value, message_type="chat_message"))
            new_message.value, new_message.focus = "", True
            page.update()

    def on_message(message: Message):
        m = (ChatMessage(message) if message.message_type == "chat_message"
             else ft.Text(message.text, italic=True, color=ft.colors.WHITE, size=12))
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    join_username = ft.TextField(
        label="Enter your name to join the chat", autofocus=True, on_submit=join_chat_click)
    page.dialog = ft.AlertDialog(
        open=True, modal=True, title=ft.Text("Welcome!"),
        content=ft.Column([join_username], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(
            text="Join chat", on_click=join_chat_click)],
        actions_alignment="end",
    )

    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    new_message = ft.TextField(hint_text="Write a message...", autofocus=True, shift_enter=True,
                               min_lines=1, max_lines=5, filled=True, expand=True, on_submit=send_message_click)

    page.add(
        ft.Container(content=chat, border=ft.border.all(
            1, ft.colors.OUTLINE), border_radius=5, padding=10, expand=True),
        ft.Row([new_message, ft.IconButton(icon=ft.icons.SEND_ROUNDED,
               tooltip="Send message", on_click=send_message_click)]),
    )


ft.app(port=8550, target=main, view=ft.WEB_BROWSER)
