from flask import Flask, Blueprint, render_template, request, session, redirect, flash, jsonify
import sqlite3
from auth_utils import requires_permission



task_manager = Blueprint('task_manager', __name__, url_prefix='/task_manager')

tasks = []

@task_manager.route('/')
def Task_Manager():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('task_manager.html', tasks=tasks)

def get_db_connection():
    conn = sqlite3.connect('nutzer.db')
    conn.row_factory = sqlite3.Row  # Ergebnisse als Dictionary-ähnliche Objekte zurückgeben
    return conn

@task_manager.route('/add_task', methods=['POST'])
@requires_permission('create_task')
def add_task():
    title = request.form['title']
    description = request.form.get('description', '')

    user_email = session.get('email') #E-Mail-Abfrage für created_by

    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, description, status, created_by) VALUES (?, ?, ?, ?)', (title, description, 'To Do', user_email))
    conn.commit()
    conn.close()

    return redirect('/task_manager')

@task_manager.route('/delete_task/<int:task_id>', methods=['POST'])
@requires_permission('delete_task')
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.execute('DELETE FROM checklist WHERE task_id = ?', (task_id,))
    conn.commit()
    conn.close()

    return redirect('/task_manager')

@task_manager.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@requires_permission('edit_task')
def edit_task(task_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

     # Rollenprüfung: Wer darf was?
    user_role = session.get('role')
    user_email = session.get('email')

    # Admins & Manager dürfen alle bearbeiten
    if user_role in ['Admin', 'Manager']:
        pass  # Keine Einschränkung

    # Benutzer dürfen nur eigene Tasks bearbeiten (falls `task['created_by']` existiert)
    elif user_role == 'Benutzer':
        task_created_by = task['created_by'] if 'created_by' in task.keys() else None  # 🔹 Stelle sicher, dass die Spalte existiert
        if not task_created_by or task_created_by != user_email:
            flash("❌ Du darfst nur deine eigenen Aufgaben bearbeiten!", "danger")
            return redirect('/task_manager')

    if request.method == 'POST':
        # Titel und Beschreibung der Aufgabe
        title = request.form['title']
        description = request.form['description']
        conn.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?', (title, description, task_id))
        
         # Alte Checklistenpunkte löschen
        # conn.execute('DELETE FROM checklist WHERE task_id = ?', (task_id,))

        checklist_items = request.form.getlist('checklist_item')
        checklist_statuses = request.form.getlist('checklist_status')
        for item, status in zip(checklist_items, checklist_statuses):
            conn.execute(
                'INSERT INTO checklist (task_id, item, status) VALUES (?, ?, ?)',
                (task_id, item, status == 'on')
            )

        conn.commit()
        conn.close()
        return redirect('/task_manager')

    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    checklist = conn.execute('SELECT * FROM checklist WHERE task_id = ?', (task_id,)).fetchall()
    conn.close()
    return render_template('edit_task.html', task=task, checklist=checklist)

@task_manager.route('/edit_task/<int:task_id>', methods=['POST'])
@requires_permission('move_task')
def edit_task_1(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Aufgabe aus der Datenbank abrufen
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    user_role = session.get('role')
    user_email = session.get('email')

    # Admins & Manager dürfen alle Aufgaben verschieben
    if user_role in ['Admin', 'Manager']:
        pass  # Keine Einschränkung

    # Benutzer dürfen nur eigene Tasks verschieben
    elif user_role == 'Benutzer':
        if 'created_by' in task.keys() and task['created_by'] != user_email:
            flash("❌ Du darfst nur deine eigenen Aufgaben verschieben!", "danger")
            return redirect('/task_manager')

    title = request.form['title']
    description = request.form['description']
    status = request.form['status']  # Neuer Status aus dem Formular
    checklist_items = request.form.getlist('checklist_item')
    checklist_status = request.form.getlist('checklist_status')

    # Speichere die Änderungen in der Datenbank
    conn = get_db_connection()
    conn.execute('''
        UPDATE tasks 
        SET title = ?, description = ?, status = ?
        WHERE id = ?
    ''', (title, description, status, task_id))
    conn.commit()

    # (Optional) Checkliste updaten (falls nötig)

    conn.close()
    return redirect('/task_manager')

@task_manager.route('/delete_checklist_item/<int:item_id>', methods=['POST'])
def delete_checklist_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Prüfen, ob das Item existiert
    cursor.execute('SELECT * FROM checklist WHERE id = ?', (item_id,))
    item = cursor.fetchone()

    if not item:
        conn.close()
        return jsonify({"ok": False, "message": "Fehler: Checklistenpunkt existiert nicht"}), 400

    # Item aus der Datenbank löschen
    cursor.execute('DELETE FROM checklist WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

    return jsonify({"ok": True, "message": "Checklistenpunkt erfolgreich gelöscht"}), 200
