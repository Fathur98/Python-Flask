from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(200), nullable=False)
    nama = db.Column(db.String(200), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    tasks = Todo.query.order_by(Todo.id).all()
    return render_template('show.html', tasks=tasks)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        alamat = request.form['alamat']
        new_task = Todo(nim=nim,nama=nama,alamat=alamat)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.id).all()
        return render_template('add.html', tasks=tasks)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.nim = request.form['nim']
        task.nama = request.form['nama']
        task.alamat = request.form['alamat']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('edit.html', task=task)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


if __name__ == "__main__":
    app.run(debug=True)