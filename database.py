import sqlite3
from datetime import datetime
import os

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ATM.db")

def obtener_conexion():
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            num_cuenta TEXT UNIQUE NOT NULL,
            pin TEXT NOT NULL,
            saldo REAL NOT NULL
        )
    ''')

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

    conn.commit()
    conn.close()

def validar_credenciales(cuenta, nip):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, saldo FROM usuarios WHERE num_cuenta = ? AND pin = ?", (cuenta, nip))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def registrar_transaccion(u_id, tipo, monto, concepto=None, destino=None):
    conn = obtener_conexion()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO transacciones (usuario_id, tipo, monto, concepto, cuenta_destino, fecha_hora)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (u_id, tipo, monto, concepto, destino, fecha))

    if tipo == "Depósito":
        cursor.execute("UPDATE usuarios SET saldo = saldo + ? WHERE id = ?", (monto, u_id))
    elif tipo in ["Retiro", "Transferencia"]:
        cursor.execute("UPDATE usuarios SET saldo = saldo - ? WHERE id = ?", (monto, u_id))

    conn.commit()
    conn.close()

def obtener_saldo(usuario_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0.0

if __name__ == "__main__":
    inicializar_db()
    print("Tablas creadas correctamente.")