import sqlite3
from datetime import datetime

DB_NAME = "ATM.db"

def obtener_conexion():
    return sqlite3.connect(DB_NAME)


def inicializar_db():
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            num_cuenta TEXT UNIQUE NOT NULL,
            pin TEXT NOT NULL,
            saldo REAL NOT NULL
        )
    ''')

    # Tabla de Transacciones (Depósitos, Retiros, Transferencias)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            tipo TEXT NOT NULL,
            monto REAL NOT NULL,
            concepto TEXT,
            cuenta_destino TEXT NOT NULL,
            fecha_hora TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')

    # Insertar 10 usuarios de prueba (solo si la tabla está vacía)
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        usuarios = [
            ('Erick Landaverde', '12345678', '1234', 5000.0),
            ('Karen González', '87654321', '4321', 12500.0),
            ('José Zúñiga', '11223344', '1111', 300.0),
            ('Osmar Hernández', '55667788', '2222', 8900.0),
            ('Azael Aceves', '99001122', '3333', 150.0),
            ('Juan Sánchez', '33445566', '4444', 25000.0),
            ('David Tirado', '77889900', '5555', 4200.0),
            ('Fernando Chairez', '22334455', '6666', 7600.0),
            ('Eduardo García', '66778899', '7777', 120.0),
            ('Paulo Regalado', '44556677', '8888', 3100.0)
        ]
        cursor.executemany("INSERT INTO usuarios (nombre, num_cuenta, pin, saldo) VALUES (?, ?, ?, ?)", usuarios)

    conn.commit()
    conn.close()


# --- FUNCIONES DE LÓGICA ---

def validar_credenciales(cuenta, nip):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, saldo FROM usuarios WHERE num_cuenta = ? AND pin = ?", (cuenta, nip))
    usuario = cursor.fetchone()
    conn.close()
    return usuario  # Retorna (id, nombre, saldo) o None


def registrar_transaccion(u_id, tipo, monto, concepto=None, destino=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Registrar el movimiento
    cursor.execute('''
        INSERT INTO transacciones (usuario_id, tipo, monto, concepto, cuenta_destino, fecha_hora)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (u_id, tipo, monto, concepto, destino, fecha))

    # 2. Actualizar el saldo del usuario
    if tipo == "Depósito":
        cursor.execute("UPDATE usuarios SET saldo = saldo + ? WHERE id = ?", (monto, u_id))
    elif tipo in ["Retiro", "Transferencia"]:
        cursor.execute("UPDATE usuarios SET saldo = saldo - ? WHERE id = ?", (monto, u_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    inicializar_db()
    print("Base de datos lista.")