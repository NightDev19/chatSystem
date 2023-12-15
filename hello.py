import flet as ft

def main(page:ft.page):
    page.add(ft.Text(value="Hello world"))

if __name__ == "__main__":
    ft.app(target=main)