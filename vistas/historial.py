import flet as ft
import database as db


def obtener_vista_historial(page: ft.Page, sesion: dict, al_volver):

    INCREMENTO = 10
    limite_actual = [10]

    def fila_transaccion(transaccion):
        tipo, monto, concepto, cuenta_destino, fecha_hora = transaccion

        iconos = {
            "Depósito":      ft.Icons.ADD_CIRCLE_OUTLINE,
            "Retiro":        ft.Icons.MONETIZATION_ON,
            "Transferencia": ft.Icons.SWAP_HORIZ,
        }

        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(iconos.get(tipo, ft.Icons.RECEIPT_LONG),
                            color=ft.Colors.WHITE, size=22),
                    ft.Column([
                        ft.Text(tipo, color=ft.Colors.WHITE, size=15,
                                weight=ft.FontWeight.BOLD),
                        ft.Text(concepto or cuenta_destino or "", color=ft.Colors.WHITE54, size=12),
                        ft.Text(fecha_hora, color=ft.Colors.WHITE38, size=11),
                    ], spacing=1),
                ], spacing=12),
                ft.Text(f"${monto:,.2f}", color=ft.Colors.WHITE, size=16,
                        weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
            border_radius=12,
            padding=ft.Padding.only(left=16, right=16, top=14, bottom=14),
        )

    lista_column = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

    def cargar_mas(e=None):
        transacciones = db.obtener_transacciones(sesion["id"], limite_actual[0])
        total = db.obtener_total_transacciones(sesion["id"])

        lista_column.controls.clear()

        if not transacciones:
            lista_column.controls.append(
                ft.Text("Sin transacciones aún.", color=ft.Colors.WHITE54,
                        size=15, text_align=ft.TextAlign.CENTER)
            )
        else:
            for t in transacciones:
                lista_column.controls.append(fila_transaccion(t))

            if limite_actual[0] < total:
                lista_column.controls.append(
                    ft.Container(
                        content=ft.Button(
                            content=ft.Text("Cargar más", size=15, color=ft.Colors.WHITE70),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.TRANSPARENT,
                                shape=ft.RoundedRectangleBorder(radius=12),
                                overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                            ),
                            on_click=lambda e: cargar_mas_click(),
                        ),
                        alignment=ft.Alignment(0, 0),
                    )
                )

        page.update()

    def cargar_mas_click():
        limite_actual[0] += INCREMENTO
        cargar_mas()

    cargar_mas()

    tarjeta = ft.Container(
        width=580,
        height=680,
        bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
        border_radius=24,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.4, ft.Colors.WHITE)),
        padding=ft.Padding.only(left=35, right=35, top=40, bottom=40),
        content=ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.HISTORY, size=48, color=ft.Colors.WHITE),
                alignment=ft.Alignment(0, 0),
            ),
            ft.Container(height=8),
            ft.Text("Historial", size=26, color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), height=30),
            ft.Container(
                content=lista_column,
                expand=True,
            ),
            ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), height=20),
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

    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=tarjeta,
    )


if __name__ == "__main__":
    db.inicializar_db()

    ANCHO_APP = 1200
    ALTO_APP = 1020

    def test(page: ft.Page):
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
                    content=obtener_vista_historial(page, sesion, al_volver=lambda: None),
                ),
            )
        )

    ft.app(target=test, assets_dir="../imagenes")