from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps
from kanban_board import kanban_board
from Task_Manager import task_manager

#Rollen-Tabelle erstellen
ROLES = {
    'Admin': ['create_task', 'delete_task', 'edit_task', 'move_task', 'assign_task', 'view'],
    'Manager': ['create_task', 'delete_task', 'edit_task', 'move_task', 'assign_task', 'view'],
    'Benutzer': ['create_task', 'edit_own_task', 'move_own_task', 'assign_own_task', 'view'],
    'Leser': ['view']
}

# Initialisierung der DB
def init_db():
    if os.path.exists('nutzer.db'):
        # os.remove('nutzer.db') # nur notwendig für Veränderungen an der DB selbst
        conn = sqlite3.connect('nutzer.db')
        cursor = conn.cursor()

        # Benutzer-Tabelle erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('Admin', 'Manager', 'Benutzer', 'Leser'))
            )
        ''')

         # Aufgaben-Tabelle erstellen (falls sie nicht existiert)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL CHECK (status IN ('To Do', 'In Progress', 'In QA', 'Done'))
            )
        ''')
        
        # Checklisten-Tabelle erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                item TEXT NOT NULL,
                status BOOLEAN NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')

        conn.commit()
        conn.close()
        print("Datenbank wurde erfolgreich eingerichtet!")
    else:
        print("Datenbank existiert bereits")
    
# Datenbank initialisieren
init_db()

#Vorgefertigte Accounts
def create_test_users():
    conn = sqlite3.connect('nutzer.db')
    cursor = conn.cursor()

    users = [
        ("admin@test.de", generate_password_hash("adminpasswort"), "Admin"),
        ("manager@test.de", generate_password_hash("managerpasswort"), "Manager"),
        ("user@test.de", generate_password_hash("userpasswort"), "Benutzer"),
        ("leser@test.de", generate_password_hash("leserpasswort"), "Leser")
    ]

    for email, hashed_password, role in users:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if not cursor.fetchone():  # Falls der Benutzer noch nicht existiert
            cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, hashed_password, role))

    conn.commit()
    conn.close()
    print("✅ Testbenutzer wurden (falls nicht vorhanden) erfolgreich erstellt!")

# Benutzer automatisch erstellen
create_test_users()



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Für Flash-Messages benötigt

# Registriere das Kanban-Board-Blueprint
app.register_blueprint(kanban_board)

# Registriere das Task_Manager-Blueprint
app.register_blueprint(task_manager)

# Startseite anzeigen
@app.route('/')
def index():
    return render_template('index2.html')

# Funktion zur Rollenprüfung
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'angemeldet' not in session or 'role' not in session:
                return redirect(url_for('login'))
            if session['role'] not in allowed_roles:
                return jsonify({'error': 'Keine Berechtigung'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Log-In für das Portal
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'angemeldet' in session:
        return redirect(url_for('kanban_board.kanban_board_view'))
        # return redirect(url_for('task_manager.Task_Manager'))

    if request.method == 'POST':  # Wenn das Formular abgesendet wird
        email = request.form['email']
        password = request.form['password']

        # Benutzerabfrage aus der DB
        conn = sqlite3.connect('nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password, role FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()

        if result:  # Wenn der Benutzer existiert
            stored_password = result[0]
            user_role = result[1]

            if check_password_hash(stored_password, password):  # Passwort überprüfen
                session['angemeldet'] = True
                session['email'] = email
                session['role'] = user_role
                print(f"✅ Login erfolgreich! Benutzer: {email}, Rolle: {user_role}")
                return redirect(url_for('kanban_board.kanban_board_view'))
               # return redirect(url_for('task_manager.Task_Manager'))  # Weiterleitung zum Task_Manager
            else:
                print("❌ Falsches Passwort für:", email)
                return render_template('login.html', error="Falsches Passwort")
        else:
            print("❌ Benutzer nicht gefunden:", email)
            return render_template('login.html', error="E-Mail nicht gefunden")
    
    return render_template('login.html')

# Registrierung für das Portal
@app.route('/registrierung', methods=['GET', 'POST'])
def registrierung():
    if 'angemeldet' in session:
        return redirect(url_for('login'))

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
    return decorated_function # Wenn doch, dann wird der Schlüssel von an- zu abgemeldet geändert

@app.route('/add_task', methods=['POST'])
@role_required(['Admin', 'Manager', 'Benutzer'])
def add_task():
    # Task-Erstellung basierend auf Rolle
    return jsonify({'message': 'Aufgabe erstellt'})

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@role_required(['Admin', 'Manager'])
def delete_task(task_id):
    # Task-Löschung basierend auf Rolle
    return jsonify({'message': 'Aufgabe gelöscht'})

@app.route('/move_task/<int:task_id>', methods=['POST'])
@role_required(['Admin', 'Manager', 'Benutzer'])
def move_task(task_id):
    # Aufgabe verschieben basierend auf Rolle
    return jsonify({'message': 'Aufgabe verschoben'})

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/ueber-uns')
def ueberuns():
    return render_template('ueber-uns.html')

if __name__ == '__main__':
    app.run(debug=True)
