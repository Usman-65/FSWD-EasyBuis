from flask import Blueprint, Flask, render_template, request, redirect

Task_Manager = Blueprint('Task_Manager', __name__)

tasks = []

@Task_Manager.route('/Task_Manager')
def index():
    return render_template('Task_Manager.html', tasks=tasks)

@Task_Manager.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form.get('description', '')
    task = {'id': len(tasks) + 1, 'title': title, 'description': description}
    tasks.append(task)
    return redirect('/')

@Task_Manager.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect('/')

@Task_Manager.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if request.method == 'POST':
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        return redirect('/')
    return render_template('edit_task.html', task=task)
