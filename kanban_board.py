from flask import Flask, Blueprint, render_template, request, redirect, session, url_for, jsonify
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
    cursor.execute("SELECT id, title, status FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    print(tasks)

    print("Geladene Aufgaben:", tasks)  # Debugging: Zeige die geladenen Aufgaben
    return render_template('kanban_board.html', tasks=tasks)


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

@kanban_board.route('/update_status', methods=['POST'])
def update_status():

    # Debugging: Zeige die empfangenen Daten
    print("Request JSON:", request.json)

    # Hole die Task-ID und den neuen Status aus der Anfrage
    task_id = request.json.get('task_id')
    new_status = request.json.get('new_status')

    # Überprüfe, ob task_id und new_status vorhanden sind
    if not task_id or not new_status:
        return jsonify({'error': 'Ungültige Daten erhalten'}), 400
    
    # Validiere den neuen Status
    if new_status not in ['To Do', 'In Progress', 'In QA', 'Done']:
        return jsonify({'error': 'Ungültiger Status'}), 400

    # Aktualisiere die Aufgabe in der Datenbank
    try:
        conn = sqlite3.connect('nutzer.db')
        cursor = conn.cursor()

        # Debugging: Prüfe, ob die Aufgabe existiert
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        print("Gefundene Aufgabe:", task)

        if not task:
            return jsonify({'error': 'Aufgabe nicht gefunden'}), 404

    # Aktualisiere den Status
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, int(task_id)))
        conn.commit()

        # Debugging: Zeige die aktualisierte Aufgabe
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        updated_task = cursor.fetchone()
        print("Aktualisierte Aufgabe:", updated_task)

        conn.close()
        return jsonify({'message': 'Status erfolgreich aktualisiert'}), 200
    except Exception as e:
        print("Fehler bei der Aktualisierung:", e)
        return jsonify({'error': 'Fehler bei der Aktualisierung'}), 500