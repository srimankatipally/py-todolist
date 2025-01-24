from flask import Blueprint, Flask, render_template, request, redirect
from sqlalchemy import select

from database import db, DATABASE_URI
from models.todo import Todo

root_blueprint = Blueprint("root", __name__)


@root_blueprint.route("/")
def index():
    todos = db.session.execute(select(Todo)).scalars()
    return render_template("index.html", todos=todos)


@root_blueprint.post("/add")
def add():
    title = request.form.get("title")

    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()

    return redirect("/")


@root_blueprint.post("/complete/<int:todo_id>")
def complete(todo_id):
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.session.execute(statement).scalar_one()
    todo.completed = True
    db.session.commit()

    return redirect("/")


@root_blueprint.post("/delete/<int:todo_id>")
def delete(todo_id):
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.session.execute(statement).scalar_one()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


def initialize_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    db.init_app(app)

    app.register_blueprint(root_blueprint)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    initialize_app().run(debug=True)
