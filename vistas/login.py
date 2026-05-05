import flet as ft
import database as db


def obtener_vista_login(page: ft.Page, al_ingresar):

    cuenta_input = ft.TextField(
        border_color=ft.Colors.WHITE38,
        focused_border_color=ft.Colors.WHITE,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        text_align=ft.TextAlign.LEFT,
        max_length=8,
        counter=ft.Container(),
        input_filter=ft.NumbersOnlyInputFilter(),
        border_radius=10,
        bgcolor=ft.Colors.TRANSPARENT,
    )

    nip_input = ft.TextField(
        border_color=ft.Colors.WHITE38,
        focused_border_color=ft.Colors.WHITE,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.LEFT,
        max_length=4,
        counter=ft.Container(),
        input_filter=ft.NumbersOnlyInputFilter(),
        border_radius=10,
        bgcolor=ft.Colors.TRANSPARENT,
    )

    error_msg = ft.Text(
        "Credenciales incorrectas",
        color=ft.Colors.RED_300,
        visible=False,
        size=13,
    )

    def intentar_login(e):
        usuario = db.validar_credenciales(cuenta_input.value, nip_input.value)
        if usuario:
            error_msg.visible = False
            sesion = {
                "id": usuario[0],
                "nombre": usuario[1],
                "saldo": usuario[2],
                "num_cuenta": cuenta_input.value,
            }
            al_ingresar(sesion)
        else:
            error_msg.visible = True
            page.update()

    tarjeta = ft.Container(
        width=420,
        bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
        border_radius=24,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.4, ft.Colors.WHITE)),
        padding=ft.Padding.only(left=40, right=40, top=45, bottom=45),
        content=ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.ACCOUNT_BALANCE, size=48, color=ft.Colors.WHITE),
                alignment=ft.Alignment(0, 0),
            ),
            ft.Container(height=8),
            ft.Text(
                "BANCO",
                size=14,
                color=ft.Colors.WHITE70,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_600,
            ),
            ft.Container(height=20),
            ft.Text(
                "Bienvenido",
                size=26,
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Container(height=25),
            ft.Text("Número de Cuenta", color=ft.Colors.WHITE70, size=13),
            ft.Container(height=5),
            cuenta_input,
            ft.Container(height=15),
            ft.Text("NIP", color=ft.Colors.WHITE70, size=13),
            ft.Container(height=5),
            nip_input,
            ft.Container(height=5),
            error_msg,
            ft.Container(height=20),
            ft.Container(
                content=ft.Button(
                    content=ft.Text("Ingresar", size=18, color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD),
                    width=340,
                    height=52,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.55, ft.Colors.BLUE_GREY_900),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    ),
                    on_click=intentar_login,
                ),
                alignment=ft.Alignment(0, 0),
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH, spacing=0),
    )

    return ft.Container(
        expand=True,
        content=ft.Column(
            [tarjeta],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


if __name__ == "__main__":
    db.inicializar_db()

    ANCHO_APP = 1200
    ALTO_APP = 1020

    def test(page: ft.Page):
        page.window.maximized = True
        page.bgcolor = ft.Colors.BLACK
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0

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
                    content=obtener_vista_login(page, al_ingresar=lambda sesion: None),
                ),
            )
        )

    ft.app(target=test, assets_dir="../imagenes")