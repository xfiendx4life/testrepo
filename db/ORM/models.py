import os
from init import *
from datetime import datetime

# worst practice
db = init_db(os.getenv("DBPATH"))

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lesson_amount = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'{self.id} {self.name}'

class Streams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'),
        nullable=False)
    course = db.relationship('Courses',
        backref=db.backref('streams', lazy=False))
    
    def __repr__(self):
        return f'course number {self.number}'

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), unique=True, nullable=False)

    streams = db.relationship('Streams', secondary='grades',
        backref=db.backref('students', lazy=False))

    def __repr__(self) -> str:
        return f"{self.id} {self.name} {self.lastname}"
    

class Grades(db.Model):
    grade = db.Column(db.Integer)
    stream = db.Column(db.Integer, db.ForeignKey('streams.id'), primary_key=True)
    student = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)




