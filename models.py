import hashlib
from init import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.id} {self.name}'
    
    def validate(self, password):
        return self.password == hashlib.md5(password.encode('utf8')).hexdigest()

    def set_password(self, password):
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    descr = db.Column(db.String(256))
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(256))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(256))

    def __repr__(self):
        return f'feedback name: {self.name}'


