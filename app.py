from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

# Initialisierung der DB
def init_db():
    if not os.path.exists('nutzer.db'):
        conn = sqlite3.connect('nutzer.db')
        cursor = conn.cursor()

        # Benutzer-Tabelle erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Aufgaben-Tabelle erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
        print("Datenbank wurde erfolgreich eingerichtet!")
    else:
        print("Datenbank existiert bereits")

# Datenbank initialisieren
init_db()


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Für Flash-Messages benötigt

# Startseite, Kanban-Board anzeigen
@app.route('/')
def index():
    if 'angemeldet' not in session:
        return redirect(url_for('login'))

    # Holen der Aufgaben aus der Datenbank
    conn = sqlite3.connect('nutzer.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, status FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    # Aufgaben an die Frontend-Vorlage übergeben
    return render_template('index2.html', tasks=tasks)

# Log-In für das Portal
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'angemeldet' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':  # Wenn das Formular abgesendet wird
        email = request.form['email']
        password = request.form['password']

        # Benutzerabfrage aus der DB
        conn = sqlite3.connect('nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()

        if result:  # Wenn der Benutzer existiert
            stored_password = result[0]
            if check_password_hash(stored_password, password):  # Passwort überprüfen
                session['angemeldet'] = True
                session['email'] = email
                return redirect(url_for('index'))  # Weiterleitung zum Kanban-Board
            else:
                return render_template('login.html', error="Falsches Passwort")
        else:
            return render_template('login.html', error="E-Mail nicht gefunden")
    
    return render_template('login.html')

# Registrierung für das Portal
@app.route('/registrierung', methods=['GET', 'POST'])
def registrierung():
    if 'angemeldet' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':  # Daten werden eingegeben
        email = request.form['email']
        password = request.form['password']

        # Prüfen, ob E-Mail bereits existiert
        conn = sqlite3.connect('nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template('registrierung.html', error="E-Mail existiert bereits.")
        
        # Passwort verschlüsseln und in die Datenbank einfügen
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('registrierung.html')

# Abmelden vom Portal
@app.route('/abmelden')
def abmelden():
    session.pop('angemeldet', None)  # Löschen des angemeldeten Status
    session.pop('email', None)
    return redirect(url_for('login'))  # Zur Login-Seite weiterleiten

# Funktion, um zu prüfen, ob der Benutzer angemeldet ist
def anmeldung_Benötigt(f): 
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'angemeldet' not in session:
            return redirect(url_for('login'))  # Wenn der Benutzer nicht angemeldet ist, zur Login-Seite
        return f(*args, **kwargs)
    return decorated_function

# Route zum Hinzufügen einer Aufgabe (Kanban-Board)
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'angemeldet' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    task_text = data['text']
    task_status = data['status']

    # Aufgabe in die Datenbank einfügen
    conn = sqlite3.connect('nutzer.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (text, status) VALUES (?, ?)", (task_text, task_status))
    conn.commit()
    conn.close()

    return '', 200  # Erfolgreiche Antwort

if __name__ == '__main__':
    app.run(debug=True)
