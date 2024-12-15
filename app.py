from flask import Flask, render_template, request, redirect, url_for
from auth import auth

app = Flask(__name__)

# Registriere das Blueprint
app.register_blueprint(auth)

# Beispiel-Daten
tasks = [
    {"id": 1, "title": "Beispielaufgabe", "description": "Beschreibung der Aufgabe"},
]

@app.route('/dashboard')
def dashboard():
    return "<h1>Willkommen im EasyBuis Dashboard!</h1>"

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/task_manager')
def task_manager():
    return render_template('Task_Manager.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    new_task = {"id": len(tasks) + 1, "title": title, "description": ""}
    tasks.append(new_task)
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>')
def edit_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return "Aufgabe nicht gefunden", 404
    return render_template('edit_task.html', task=task)

@app.route('/update_task', methods=['POST'])
def update_task():
    task_id = int(request.form.get('id'))
    title = request.form.get('title')
    description = request.form.get('description')

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            task["description"] = description
            break

    return "<script>window.close();</script>"  # Schließt das Fenster nach dem Speichern

if __name__ == '__main__':
    app.run()
