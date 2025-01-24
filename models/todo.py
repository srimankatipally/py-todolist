from models.base import BaseModel
from database import database

class Todo(BaseModel):
    __tablename__ = "todos"

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    completed = database.Column(database.Boolean, default=False)
