from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from app.shop.handlers import index

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# db.create_all()

