from flask_sqlalchemy import SQLAlchemy

from models.base import Base as BaseModel

DATABASE_URI = "sqlite:///todolist.db"

db = SQLAlchemy(model_class=BaseModel)
