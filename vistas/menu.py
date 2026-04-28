import flet as ft
import database as db
from datetime import datetime


def obtener_vista_menu(page: ft.Page, sesion: dict, al_salir):

    saldo_texto = ft.Text(
        f"${db.obtener_saldo(sesion['id']):,.2f}",
        size=42,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    ahora = datetime.now().strftime("%d/%m/%Y  %H:%M")

    def boton_menu(texto, icono, on_click):
        return ft.Container(
            content=ft.Row([
                ft.Text(texto, size=22, color=ft.Colors.WHITE),
                ft.Icon(icono, color=ft.Colors.WHITE, size=34),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
            border_radius=14,
            padding=ft.Padding.only(left=25, right=25, top=32, bottom=32),
            expand=True,
            on_click=on_click,
            ink=True,
        )

    def ir_deposito(e):
        from vistas.deposito import obtener_vista_deposito
        contenido.content = obtener_vista_deposito(page, sesion, al_volver=volver_al_menu)
        page.update()

    def ir_retiro(e):
        from vistas.retiro import obtener_vista_retiro
        contenido.content = obtener_vista_retiro(page, sesion, al_volver=volver_al_menu)
        page.update()

    def ir_transferencia(e):
        from vistas.transferencia import obtener_vista_transferencia
        contenido.content = obtener_vista_transferencia(page, sesion, al_volver=volver_al_menu)
        page.update()

    def ir_historial(e):
        from vistas.historial import obtener_vista_historial
        contenido.content = obtener_vista_historial(page, sesion, al_volver=volver_al_menu)
        page.update()

    def ir_cambiar_nip(e):
        from vistas.cambiar_nip import obtener_vista_cambiar_nip
        contenido.content = obtener_vista_cambiar_nip(page, sesion, al_volver=volver_al_menu)
        page.update()

    def cerrar_sesion(e):
        al_salir()

    def volver_al_menu():
        saldo_texto.value = f"${db.obtener_saldo(sesion['id']):,.2f}"
        contenido.content = vista_menu
        page.update()

    tarjeta = ft.Container(
        width=1100,
        bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
        border_radius=24,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.4, ft.Colors.WHITE)),
        padding=ft.Padding.only(left=50, right=50, top=45, bottom=45),
        content=ft.Column([
            ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.ACCOUNT_BALANCE, color=ft.Colors.WHITE, size=36),
                    ft.Text("BANCO", size=26, color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD),
                ], spacing=12),
                ft.Column([
                    ft.Text(ahora, color=ft.Colors.WHITE54, size=15),
                    ft.Text(sesion["nombre"], color=ft.Colors.WHITE70, size=16),
                ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=4),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), height=35),

            ft.Text("Saldo disponible", color=ft.Colors.WHITE54, size=16,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=6),
            saldo_texto,

            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), height=35),

            ft.Row([
                boton_menu("Depósito",      ft.Icons.ADD_CIRCLE_OUTLINE, ir_deposito),
                boton_menu("Retiro",        ft.Icons.MONETIZATION_ON,    ir_retiro),
                boton_menu("Transferencia", ft.Icons.SWAP_HORIZ,         ir_transferencia),
            ], spacing=15),
            ft.Container(height=15),
            ft.Row([
                boton_menu("Historial",   ft.Icons.HISTORY, ir_historial),
                boton_menu("Cambiar NIP", ft.Icons.LOCK,    ir_cambiar_nip),
                boton_menu("Salir",       ft.Icons.LOGOUT,  cerrar_sesion),
            ], spacing=15),
        ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH, spacing=0),
    )

    vista_menu = ft.Container(
        expand=True,
        content=ft.Column(
            [tarjeta],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    contenido = ft.Container(content=vista_menu, expand=True)
    return contenido


if __name__ == "__main__":
    ANCHO_APP = 1200
    ALTO_APP = 1020

    def test(page: ft.Page):
        db.inicializar_db()
        page.window.maximized = True
        page.window.full_screen = True
        page.bgcolor = ft.Colors.BLACK
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0

        sesion = {"id": 1, "nombre": "Erick Landaverde", "saldo": 5000.0, "num_cuenta": "12345678"}

        page.add(
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.Alignment(0, 0),
                content=ft.Container(
                    width=ANCHO_APP,
                    height=ALTO_APP,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    image=ft.DecorationImage(src="1.jpg", fit="cover", opacity=0.4),
                    content=obtener_vista_menu(page, sesion, al_salir=lambda: None),
                ),
            )
        )

    ft.app(target=test, assets_dir="../imagenes")