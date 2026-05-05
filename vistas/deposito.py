import flet as ft
import database as db
import asyncio


def obtener_vista_deposito(page: ft.Page, sesion: dict, al_volver):

    monto_input = ft.TextField(
        border_color=ft.Colors.WHITE38,
        focused_border_color=ft.Colors.WHITE,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        text_align=ft.TextAlign.LEFT,
        input_filter=ft.NumbersOnlyInputFilter(),
        border_radius=10,
        bgcolor=ft.Colors.TRANSPARENT,
    )

    error_msg = ft.Text("", size=14, color=ft.Colors.RED_300,
                        text_align=ft.TextAlign.CENTER, visible=False)

    def mostrar_exito(monto):
        pantalla_exito = ft.Container(
            expand=True,
            content=ft.Column([
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=100, color=ft.Colors.WHITE),
                ft.Container(height=20),
                ft.Text("¡Depósito realizado!", size=36, color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.Text(f"${monto:,.2f}", size=48, color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.Text("Regresando al menú...", size=16, color=ft.Colors.WHITE54,
                        text_align=ft.TextAlign.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER,
               horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        )
        contenedor_raiz.content = pantalla_exito
        page.update()

        async def regresar():
            await asyncio.sleep(3)
            al_volver()
            page.update()

        page.run_task(regresar)

    def confirmar(e):
        if not monto_input.value or int(monto_input.value) <= 0:
            error_msg.value = "Ingresa un monto válido."
            error_msg.visible = True
            page.update()
            return

        monto = float(monto_input.value)
        db.registrar_transaccion(sesion["id"], "Depósito", monto, destino=sesion["num_cuenta"])
        mostrar_exito(monto)

    tarjeta = ft.Container(
        width=500,
        bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
        border_radius=24,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.4, ft.Colors.WHITE)),
        padding=ft.Padding.only(left=40, right=40, top=45, bottom=45),
        content=ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, size=48, color=ft.Colors.WHITE),
                alignment=ft.Alignment(0, 0),
            ),
            ft.Container(height=8),
            ft.Text("Depósito", size=26, color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), height=30),
            ft.Text("Saldo disponible", color=ft.Colors.WHITE54, size=13,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=4),
            ft.Text(f"${db.obtener_saldo(sesion['id']):,.2f}", size=22, color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), height=30),
            ft.Text("Monto a depositar", color=ft.Colors.WHITE70, size=15),
            ft.Container(height=5),
            monto_input,
            ft.Container(height=5),
            error_msg,
            ft.Container(height=20),
            ft.Container(
                content=ft.Button(
                    content=ft.Text("Confirmar", size=18, color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD),
                    width=420,
                    height=52,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.55, ft.Colors.BLUE_GREY_900),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    ),
                    on_click=confirmar,
                ),
                alignment=ft.Alignment(0, 0),
            ),
            ft.Container(height=12),
            ft.Container(
                content=ft.Button(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.WHITE70, size=20),
                        ft.Text("Volver", size=16, color=ft.Colors.WHITE70),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    width=420,
                    height=48,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.TRANSPARENT,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    ),
                    on_click=lambda e: al_volver(),
                ),
                alignment=ft.Alignment(0, 0),
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH, spacing=0),
    )

    vista_formulario = ft.Container(
        expand=True,
        content=ft.Column(
            [tarjeta],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    contenedor_raiz = ft.Container(content=vista_formulario, expand=True)
    return contenedor_raiz


if __name__ == "__main__":
    db.inicializar_db()

    ANCHO_APP = 1200
    ALTO_APP = 1020

    def test(page: ft.Page):
        page.window.maximized = True
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
                    content=obtener_vista_deposito(page, sesion, al_volver=lambda: None),
                ),
            )
        )

    ft.app(target=test, assets_dir="../imagenes")