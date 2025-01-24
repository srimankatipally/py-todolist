# Flask To-Do List Application

This is a simple to-do list application built with Flask and SQLAlchemy. It allows users to add, complete, and delete tasks.

## Features

- Add new tasks
- Mark tasks as completed
- Delete tasks
- View all tasks

## Prerequisites

- Python 3.9 or higher
- Virtualenv (optional but recommended)

## Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/py-todolist.git
cd py-todolist
```

2. **Create a Virtual Environment**

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate # On Windows use .venv\Scripts\activate
```

3. **Install Dependencies**

Install the required Python packages using pip.

```bash
pip install -r requirements.txt
```

4. **Run the Application**

Start the Flask development server.

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## Project Structure

- `app.py`: Main application file where the Flask app is initialized.
- `models/`: Directory containing SQLAlchemy models.
- `templates/`: HTML templates for rendering views.
- `database.py`: Database configuration and initialization.
- `requirements.txt`: List of Python dependencies.
