from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Settings:
    def __init__(self):
        self.app = self.return_server()
        self.db = self.return_database()
    def return_server(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
        return app

    def return_database(self):
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(self.app)
        return db