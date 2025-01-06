from flask import Flask, Blueprint, render_template, request, redirect, session, url_for
import sqlite3

kanban_board = Blueprint('kanban_board', __name__, url_prefix='/kanban_board')

tasks = []

@kanban_board.route('/')
def kanban_board_view():
    if 'angemeldet' not in session:
        return redirect(url_for('login'))

    # Aufgaben aus der Datenbank laden
    conn = sqlite3.connect('nutzer.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    return render_template('kanban_board.html', tasks=tasks)


    # Aufgaben an die Frontend-Vorlage übergeben
 #   return render_template('index2.html', tasks=tasks)

   # Aufgaben-Tabelle erstellen
#        cursor.execute('''
#            CREATE TABLE IF NOT EXISTS tasks (
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                text TEXT NOT NULL,
#                status TEXT NOT NULL
#            )
#        ''')

# Route zum Hinzufügen einer Aufgabe (Kanban-Board)
@kanban_board.route('/add_task', methods=['POST'])
def add_task():
    if 'angemeldet' not in session:
        return redirect(url_for('kanban_board'))

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