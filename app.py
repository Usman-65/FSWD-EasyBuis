from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

#Initialisierung der DB
def init_db():
    if not os.path.exists('Nutzer.db'):
        conn = sqlite3.connect('Nutzer.db') #Erstellt Datenbank, if not exists
        cursor = conn.cursor()

        #Initialisierung der Tabelle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                E-Mail TEXT UNIQUE NOT NULL,
                Password TEXT NOT NULL
            )    
        ''')
        conn.commit()
        conn.close()
        print("Datenbank wurde erfolgreich Eingerichtet!")
    else:
        print("Datenbank existiert bereits")

#Initialisierung        
init_db()

#App Start
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Für Flash-Messages benötigt

@app.route('/')
def index():
    return render_template('index.html')

#Log-In für das Portal
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'angemeldet' in session:
        return render_template('login.html', info="Du bist bereits angemeldet.")
    
    if request.method == 'POST':  # Wenn das Formular abgesendet wird
        email = request.form['email']  # Abfrage der E-Mail und des Passwortes
        password = request.form['password']
     
        conn = sqlite3.connect('nutzer.db') # Datenbankabfrage
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()

        if result:  # Wenn der Benutzer existiert
            stored_password = result[0]  # Pull des gespeicherten Passwort
            if check_password_hash(stored_password, password):  # Passwort überprüfen
                session['angemeldet'] = True
                session['email'] = email
                return redirect(url_for('task_manager'))  # Zum Programm weiterleiten, wenn korekt
            else:
                return render_template('login.html', error="Falsches Passwort")  # Fehlermeldung bei falschem Passwort
        else:
            return render_template('login.html', error="E-Mail nicht gefunden")  # Fehlermeldung bei E-Mail nicht gefunden
    
    return render_template('login.html')

#Regisrtrierung zum Portal
@app.route('/registrierung', methods=['GET', 'POST'])
def registrierung():
    if 'angemeldet' in session:
        return render_template('registrierung.html', info="Du bist bereits angemeldet.")


    if request.method == 'POST': # Erst Eingabe der Daten
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('nutzer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,)) # Suche nach E-Mail, ob sie bereits existiert
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template('registrierung.html', error="E-Mail existiert bereits.") # Fehlermeldung, wenn die Nutzerdaten bereits existieren
        
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password)) # Eingabe der Daten, Passwort wird verschlüsselt
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('registrierung.html')

# Abmelde-Funktion
@app.route('/abmelden')
def abmelden():
    session.pop('angemeldet', None) #Löscht den Status "angemeldet" und die Email aus der Session 
    session.pop('email', None)
    return redirect(url_for('login')) # Redirect zur Log-In Seite

# Prüft ob Benutzer angemeldet ist
def anmeldung_Benötigt(f): 
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'angemeldet' not in session:
            return redirect(url_for('login')) # Wenn der Benutzer nicht mehr angemeldet ist, dann wird er zum Login umgeleitet
        return f(*args, **kwargs)
    return decorated_function # Wenn doch, dann wird der Schlüssel von an- zu abgemeldet geändert

if __name__ == '__main__':
    app.run(debug=True)
