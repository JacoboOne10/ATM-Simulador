import flet as ft
from database import inicializar_db
from vistas.login import obtener_vista_login
from vistas.menu import obtener_vista_menu

ANCHO_APP = 1200
ALTO_APP = 1020


def main(page: ft.Page):
    inicializar_db()
    page.window.maximized = True
    page.window.full_screen = True
    page.bgcolor = ft.Colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    contenido = ft.Container(expand=True)

    def ir_a_login(e=None):
        contenido.content = obtener_vista_login(page, al_ingresar=entrar_a_app)
        page.update()

    def entrar_a_app(sesion):
        contenido.content = obtener_vista_menu(page, sesion, al_salir=ir_a_login)
        page.update()

    caja = ft.Container(
        width=ANCHO_APP,
        height=ALTO_APP,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        image=ft.DecorationImage(src="1.jpg", fit="cover", opacity=0.4),
        content=contenido,
    )

    page.add(
        ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            alignment=ft.Alignment(0, 0),
            content=caja,
        )
    )
    ir_a_login()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="imagenes")