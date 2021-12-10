from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def init_db(path):
    app = Flask(__name__) # объект приложения Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = path # привязываем базу данных
    db = SQLAlchemy(app) # создаем объект SQLAlchemy
    return db

def create_db(db):
    db.create_all()

