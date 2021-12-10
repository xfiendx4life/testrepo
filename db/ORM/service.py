from models import *

def createStudent(name, lastname):
    st = Students(name=name, lastname=lastname)
    db.session.add(st)
    return st

def addCourse(name, lesson_amount):
    c = Courses(name=name, lesson_amount=lesson_amount)
    db.session.add(c)
    return c

def addStreams(number, course, start_date=datetime.now()):
    str = Streams(number=number, course=course, start_date=start_date)
    db.session.add(str)
    return str

def addGrades(grade: int, student: Students, stream: Streams):
    student.streams.append(stream)
    Grades.query.filter_by(student=student.id).filter_by(stream=stream.id).first().grade = grade

