import os
import sqlite3
import datetime
import uuid
from flask import Flask, request, render_template_string, redirect, url_for, session, send_from_directory

# --- CONFIGURAÇÕES ---
PASTA_BASE = os.getenv("DATA_DIR", "qrcode_registros")
os.makedirs(PASTA_BASE, exist_ok=True)
DB_FILE = os.path.join(PASTA_BASE, 'reservas.db')
MANAGER_SECRET_CODE = 'GESTORTJRS0830'

LOGO_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(LOGO_FOLDER, exist_ok=True)
LOGO_FILENAME = "unica_logo.png"

# --- BANCO DE DADOS ---
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            team TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            room TEXT NOT NULL,
            desk INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    cursor.execute("SELECT COUNT(user_id) FROM users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ('guri1', 'senha123', 'Funcionario Um', 'Time de Desenvolvimento', 'user'),
            ('guri2', 'senha456', 'Time de Vendas', 'Time de Vendas', 'user'),
            ('gestor1', 'admin123', 'Gestor Chefe', 'Gerência', 'manager')
        ]
        cursor.executemany(
            "INSERT INTO users (user_id, password, name, team, role) VALUES (?, ?, ?, ?, ?)",
            default_users
        )
    conn.commit()
    conn.close()

# --- APLICAÇÃO ---
app = Flask(__name__)

# Garante que o banco/estrutura exista também sob Gunicorn/Render
init_db()
app.secret_key = os.environ.get("SECRET_KEY", str(uuid.uuid4()))
rooms = {
    '1703': {'desks': 20}, '2107': {'desks': 20},
    '2203': {'desks': 20}, '2207': {'desks': 20}
}

html_template = "<h1>UNICAA - Sistema de Reserva de Mesas</h1>"

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/logo_file')
def logo_file():
    return send_from_directory(LOGO_FOLDER, LOGO_FILENAME)

if __name__ == '__main__':
    init_db()
    # No Render não usamos Pyngrok
    if os.environ.get("RENDER") == "true":
        app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    else:
        try:
            from pyngrok import ngrok
            public_url = ngrok.connect(5000)
            print(f" * Ngrok Tunnel: {public_url}")
        except Exception as e:
            print(f"Ngrok indisponível: {e}")
        app.run(host='0.0.0.0', port=5000)
