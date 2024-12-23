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
    conn.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    conn.close()

    return redirect('/task_manager')

@task_manager.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

    return redirect('/task_manager')

@task_manager.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        conn.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?', (title, description, task_id))
        conn.commit()
        conn.close()
        return redirect('/task_manager')

    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    return render_template('edit_task.html', task=task)