from service import *

s = createStudent("punk", "dirty")
c = addCourse("sqLAlchemy", 4)
st = addStreams(45, c)
db.session.commit()
addGrades(5, s, st)
db.session.commit()