from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretinis_raktas'

# Duomenų saugojimas
tasks = []
users = []

# Pagalbinės funkcijos
def get_task_by_id(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

# Maršrutai
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    user = request.form['user']
    
    # Tikriname, ar visi formos laukai užpildyti
    if not title or not description or not status or not user:
        return redirect(url_for('index'))
    
    task_id = len(tasks) + 1
    tasks.append({'id': task_id, 'title': title, 'description': description, 'status': status, 'user': user})
    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>', methods=['POST', 'GET'])
def edit_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        task['status'] = request.form['status']
        task['user'] = request.form['user']
        return redirect(url_for('index'))
    
    return render_template('edit_task.html', task=task)

@app.route('/change_status/<int:task_id>/<new_status>', methods=['POST'])
def change_status(task_id, new_status):
    task = get_task_by_id(task_id)
    if not task:
        return redirect(url_for('index'))
    
    task['status'] = new_status
    return redirect(url_for('index'))

# Naujas maršrutas nukreipiantis tiesiai į stilių failą
@app.route('/styles')
def styles():
    return app.send_static_file('styles.css')

if __name__ == '__main__':
    app.run(debug=True)
