import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACT_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=["GET", "POST"])

def Home():
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)


@app.route('/add', methods=["GET", "POST"])
def create():
    if request.method == 'POST':
        print(request.form['title'])
        todo = Todo(title=request.form['title'], desc = request.form['desc'])
        db.session.add(todo)
        db.session.commit()
    return redirect('/')

@app.route('/update/int<sno>')
def update():
    pass

@app.route('/delete/<int:sno>')
def delete(sno):
    todo  = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)