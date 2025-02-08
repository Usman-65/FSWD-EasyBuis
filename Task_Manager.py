from flask import Flask, Blueprint, render_template, request, redirect
import sqlite3

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
def add_task():
    title = request.form['title']
    description = request.form.get('description', '')

    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)', (title, description, 'To Do'))
    conn.commit()
    conn.close()

    return redirect('/task_manager')

@task_manager.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.execute('DELETE FROM checklist WHERE task_id = ?', (task_id,))
    conn.commit()
    conn.close()

    return redirect('/task_manager')

@task_manager.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = get_db_connection()

    if request.method == 'POST':
        # Titel und Beschreibung der Aufgabe
        title = request.form['title']
        description = request.form['description']
        conn.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?', (title, description, task_id))
        
         # Alte Checklistenpunkte löschen
        conn.execute('DELETE FROM checklist WHERE task_id = ?', (task_id,))

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
def edit_task_1(task_id):
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
