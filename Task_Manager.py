from flask import Flask, Blueprint, render_template, request, redirect

app = Flask(__name__)

task_manager = Blueprint('task_manager', url_prefix='/task_manager')

tasks = []

@task_manager.route('/task_manager')
def index():
    return render_template('index.html', tasks=tasks)

@task_manager.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form.get('description', '')
    task = {'id': len(tasks) + 1, 'title': title, 'description': description}
    tasks.append(task)
    return redirect('/')

@task_manager.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect('/')

@task_manager.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if request.method == 'POST':
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        return redirect('/')
    return render_template('edit_task.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)
