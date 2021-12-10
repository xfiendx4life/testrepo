import unittest

from service import *


class TestORM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = db
        create_db(cls.db)

    @classmethod
    def tearDownClass(cls):
        db.session.close()
        cls.db.drop_all()
    

    def tearDown(self) -> None:
        self.db.session.rollback()
        Courses.query.delete()
        Students.query.delete()
        Streams.query.delete()
        

    def test_createStudentNoCommit(self):
        st = createStudent('testname', "testlastname")
        # print(Students.query.all())
        self.assertEqual(Students.query.one(), st)

    def test_createStudentWithCommit(self):
        st = createStudent('testname', "testlastname")
        # print(Students.query.all())
        self.db.session.commit()
        self.assertEqual(Students.query.one(), st)
        db.session.delete(st)
    
    def test_addCourse(self):
        c = addCourse('testcourse', 4)
        self.db.session.commit()
        self.assertEqual(c, Courses.query.one())
        
    
    def test_course_and_streams(self):
        c = addCourse('testcourse', 4)
        st = addStreams(45, c)
        self.db.session.commit()
        self.assertEqual(st, Streams.query.one())
        self.assertEqual(c, Streams.query.one().course)