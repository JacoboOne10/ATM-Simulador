import flet as ft
import database as db


def login_screen(page: ft.Page):
    # --- CONFIGURACIÓN DE PÁGINA ---
    page.window_maximized = True
    page.bgcolor = ft.Colors.BLACK
    page.title = "Simulador ATM - Login"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.margin = 0

    # --- ESTILO PARA EL BOTÓN
    estilo_comun = ft.ButtonStyle(
        bgcolor=ft.Colors.BLACK,
        color=ft.Colors.WHITE,
        shape=ft.RoundedRectangleBorder(radius=10),
        side=ft.BorderSide(width=0, color=ft.Colors.TRANSPARENT),
    )

    # --- FUNCIÓN PARA LA SOMBRA PERIMETRAL (GLOW) ---
    def aplicar_sombra_perimetral(control):
        return ft.Container(
            content=control,
            border_radius=10,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(
                spread_radius=3,      # grosor
                blur_radius=10,       # que se difumine más suave
                color=ft.Colors.with_opacity(0.65, ft.Colors.WHITE), # que sea más blanco
                offset=ft.Offset(0, 0),
            ),
        )

    # --- CAMPOS DE ENTRADA (Hint Text - Se quita al clic) ---
    cuenta_input = ft.TextField(
        hint_text="Número de Cuenta",
        hint_style=ft.TextStyle(color=ft.Colors.WHITE70),
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color=ft.Colors.TRANSPARENT,
        bgcolor=ft.Colors.BLACK,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        width=400,
        text_align=ft.TextAlign.CENTER,
        max_length=8,
        counter=ft.Container(),
        input_filter=ft.NumbersOnlyInputFilter(),
        border_radius=10,
    )

    nip_input = ft.TextField(
        hint_text="NIP",
        hint_style=ft.TextStyle(color=ft.Colors.WHITE70),
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color=ft.Colors.TRANSPARENT,
        bgcolor=ft.Colors.BLACK,
        color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        password=True,
        can_reveal_password=True,
        width=400,
        text_align=ft.TextAlign.CENTER,
        max_length=4,
        counter=ft.Container(),
        input_filter=ft.NumbersOnlyInputFilter(),
        border_radius=10,
    )

    error_msg = ft.Text("Credenciales incorrectas", color="red", visible=False, size=18)

    def intentar_login(e):
        usuario = db.validar_credenciales(cuenta_input.value, nip_input.value)
        if usuario:
            error_msg.visible = False
            page.snack_bar = ft.SnackBar(ft.Text(f"Acceso Concedido: {usuario[1]}"))
            page.snack_bar.open = True
            page.update()
        else:
            error_msg.visible = True
            page.update()

    # --- ENSAMBLADO FINAL ---
    fondo_principal = ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src="1.jpg",
            fit="cover",
            opacity=0.4
        ),
        content=ft.Column([
            # Espaciado superior para centrar el formulario
            ft.Container(height=20),

            aplicar_sombra_perimetral(cuenta_input),
            ft.Container(height=15),
            aplicar_sombra_perimetral(nip_input),

            error_msg,
            ft.Container(height=25),

            # Botón Ingresar
            aplicar_sombra_perimetral(
                ft.FilledButton(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Text("Ingresar", size=22, color=ft.Colors.WHITE),
                            ft.Icon(ft.Icons.LOGIN, size=35, color=ft.Colors.WHITE),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        alignment=ft.Alignment(0, 0)
                    ),
                    height=80,
                    width=400,
                    style=estilo_comun,
                    on_click=intentar_login
                )
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
    )

    page.add(fondo_principal)
    page.update()


if __name__ == "__main__":
    db.inicializar_db()
    ft.run(login_screen, assets_dir="../imagenes")