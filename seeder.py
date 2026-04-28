from database import obtener_conexion, inicializar_db

def seed():
    inicializar_db()  # Asegura que las tablas existan

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] > 0:
        print("La base de datos ya tiene usuarios. Seeder omitido.")
        conn.close()
        return

    usuarios = [
        ('Erick Landaverde',   '12345678', '1234', 5000.0),
        ('Karen González',     '87654321', '4321', 12500.0),
        ('José Zúñiga',        '11223344', '1111', 300.0),
        ('Osmar Hernández',    '55667788', '2222', 8900.0),
        ('Azael Aceves',       '99001122', '3333', 150.0),
        ('Juan Sánchez',       '33445566', '4444', 25000.0),
        ('David Tirado',       '77889900', '5555', 4200.0),
        ('Fernando Chairez',   '22334455', '6666', 7600.0),
        ('Eduardo García',     '66778899', '7777', 120.0),
        ('Paulo Regalado',     '44556677', '8888', 3100.0),
    ]

    cursor.executemany(
        "INSERT INTO usuarios (nombre, num_cuenta, pin, saldo) VALUES (?, ?, ?, ?)",
        usuarios
    )
    conn.commit()
    conn.close()
    print(f"{len(usuarios)} usuarios insertados correctamente.")

if __name__ == "__main__":
    seed()