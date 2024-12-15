from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

#Initialisierung der DB
def init_db():
    if not os.path.exists('Nutzer.db'):
        conn = sqlite3.connect('Nutzer.db')
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

USER_EMAIL = "test@easybuis.de"
USER_PASSWORD = "password123"

@app.route('/')
def Start():
    return render_template('index.html')

#Registirerung auf der Seite
@app.route('/Registrierung', methods=['GET', 'POST'])
def registrierung():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Eingaben prüfen
        if not email or not password or not confirm_password:
            flash("Bitte alle Felder ausfüllen.", "error")
            return redirect(url_for('registrierung'))

        if password != confirm_password:
            flash("Passwörter stimmen nicht überein.", "error")
            return redirect(url_for('registrierung'))

        try:
            # Verbindung zur Datenbank
            conn = sqlite3.connect('Nutzer.db')
            cursor = conn.cursor()

            # Überprüfen, ob die E-Mail bereits existiert
            cursor.execute("SELECT * FROM users WHERE EMail = ?", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Diese E-Mail ist bereits registriert.", "error")
                conn.close()
                return redirect(url_for('registrierung'))

            # Benutzer registrieren
            cursor.execute("INSERT INTO users (EMail, Password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()

            flash("Registrierung erfolgreich! Sie können sich jetzt einloggen.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Ein Fehler ist aufgetreten: {str(e)}", "error")
            return redirect(url_for('registrierung'))

    return render_template('Registirerung.html')

#Log-In für die Seite
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        accept = request.form.get('accept')

        if not accept:
            flash("Bitte akzeptieren Sie die Nutzungsbedingungen.", "error")
            return redirect(url_for('login'))

        if email == USER_EMAIL and password == USER_PASSWORD:
            flash("Erfolgreich eingeloggt!", "success")
            return redirect(url_for('task_manager')) #Direkte Weiterleitung auf den Task_Manager nach Erfolgreichem Log-In 
        else:
            flash("Ungültige E-Mail oder Passwort.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/Task_Manager')
def Task_Manager():
    return render_template('Task_Manager.html')

if __name__ == '__main__':
    app.run(debug=True)
