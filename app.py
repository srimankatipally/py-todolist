from flask import Blueprint, Flask, render_template, request, redirect
from sqlalchemy import select, func, update

from database import db, DATABASE_URI
from models.todo import Todo

root_blueprint = Blueprint("root", __name__)


@root_blueprint.route("/")
def index():
    todos = db.session.execute(select(Todo).order_by(Todo.position)).scalars()
    return render_template("index.html", todos=todos)


@root_blueprint.post("/add")
def add():
    title = request.form.get("title")
    
    # Get the maximum position and add 1 for the new item
    max_position = db.session.execute(func.coalesce(func.max(Todo.position), -1)).scalar() + 1
    
    new_todo = Todo(title=title, position=max_position)
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
    # Get the todo to be deleted
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.session.execute(statement).scalar_one()
    
    # Get the position of the todo to be deleted
    position = todo.position
    
    # Delete the todo
    db.session.delete(todo)
    
    # Update the positions of todos below the deleted one
    db.session.execute(
        update(Todo)
        .where(Todo.position > position)
        .values(position=Todo.position - 1)
    )
    
    db.session.commit()
    return redirect("/")


@root_blueprint.post("/move_up/<int:todo_id>")
def move_up(todo_id):
    # Get the current todo
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.session.execute(statement).scalar_one()
    
    # If already at the top, do nothing
    if todo.position <= 0:
        return redirect("/")
    
    # Get the todo above (with position one less)
    above_todo = db.session.execute(
        select(Todo).where(Todo.position == todo.position - 1)
    ).scalar_one_or_none()
    
    if above_todo:
        # Swap positions
        above_todo.position, todo.position = todo.position, above_todo.position
        db.session.commit()
    
    return redirect("/")


@root_blueprint.post("/move_down/<int:todo_id>")
def move_down(todo_id):
    # Get the current todo
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.session.execute(statement).scalar_one()
    
    # Get the todo below (with position one more)
    below_todo = db.session.execute(
        select(Todo).where(Todo.position == todo.position + 1)
    ).scalar_one_or_none()
    
    if below_todo:
        # Swap positions
        below_todo.position, todo.position = todo.position, below_todo.position
        db.session.commit()
    
    return redirect("/")


def initialize_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    db.init_app(app)

    app.register_blueprint(root_blueprint)

    with app.app_context():
        db.create_all()
        
        # Initialize positions for existing todos if position is not set
        todos = db.session.execute(
            select(Todo).where(Todo.position == 0).order_by(Todo.id)
        ).scalars().all()
        
        for i, todo in enumerate(todos):
            todo.position = i
        
        db.session.commit()

    return app


if __name__ == "__main__":
    initialize_app().run(debug=True)
