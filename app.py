from flask import Blueprint, Flask, render_template, request, redirect, url_for

from models.todo import Todo
from database import DATABASE_URL, database

root_blueprint = Blueprint('root', __name__)
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@root_blueprint.route('/')
def index():
    todos = database.session.execute(database.select(Todo)).scalars()
    return render_template('index.html', todos=todos)

@api_blueprint.post('/add')
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title)
    database.session.add(new_todo)
    database.session.commit()
    return redirect(url_for('api.index'))

@api_blueprint.post('/complete/<int:todo_id>')
def complete(todo_id):
    todo = database.session.execute(database.select(Todo).where(Todo.id == todo_id)).scalar_one()
    todo.completed = True
    database.session.commit()
    return redirect(url_for('api.index'))

@api_blueprint.post('/delete/<int:todo_id>')
def delete(todo_id):
    todo = database.session.execute(database.select(Todo).where(Todo.id == todo_id)).scalar_one()
    database.session.delete(todo)
    database.session.commit()
    return redirect(url_for('api.index'))

def initialize_app():
	app = Flask(__name__)
	app.register_blueprint(root_blueprint)
	app.register_blueprint(api_blueprint)

	app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	database.init_app(app)

	with app.app_context():
		database.create_all(bind=None)

	return app

if __name__ == '__main__':
    initialize_app().run(debug=True)

