# db_init.py
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the Flask app with the SQLAlchemy object.
    Creates all tables if they don't already exist.
    """
    db.init_app(app)
    
    # Optional: Create all tables
    with app.app_context():
        db.create_all()
