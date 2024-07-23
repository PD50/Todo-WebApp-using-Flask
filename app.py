from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()



class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.task}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    if request.method == 'POST':
        task = request.form['task']
        desc = request.form['desc']
        todo = Todo(task = task, desc = desc)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo = alltodo)

@app.route('/delete/<int:sno>')
def delete_todo(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        task = request.form['task']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.task = task
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo )

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
