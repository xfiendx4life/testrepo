from p import *
import unittest

class Testdb(unittest.TestCase):
    @classmethod 
    def setUpClass(cls):
        cls.db = DB(path=":memory:")
        cursor = cls.db.newCursor()
        cls.db.cursor.executescript('''CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        lessons_amount INTEGER
        );
        CREATE TABLE streams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER NOT NULL UNIQUE,
        course_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        FOREIGN KEY (course_id) REFERENCES courses(id)
        );
        CREATE TABLE grades (
            student_id INTEGER,
            stream_id INTEGER, 
            grade INTEGER,
            PRIMARY KEY (student_id, stream_id),
            FOREIGN KEY (student_id) REFERENCES "students"(id),
            FOREIGN KEY (stream_id) REFERENCES streams(id));
        CREATE TABLE IF NOT EXISTS "students" (
            "id"	INTEGER,
            "name"	text,
            "lastname"	TEXT birth_date TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        ''')
        cls.db._connection.commit()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.db._connection.close()
    
    def setUp(self) -> None:
        self.db.newCursor()
        self.db.cursor.execute("INSERT INTO students(name, lastname) VALUES (?, ?);",
            ("John", "Doe"))
        self.test_id = self.db.cursor.lastrowid
        self.db.cursor.execute("INSERT INTO grades(student_id, stream_id, grade) VALUES (?, 2, 5);",
            (self.test_id,))
        self.db._connection.commit()

    def tearDown(self):
        self.db.cursor.execute("DELETE FROM grades WHERE student_id=?;", (self.test_id,))
        self.db.cursor.execute("DELETE FROM students WHERE id=?;", (self.test_id, ))
        self.db._connection.commit()
        self.db.cursor.close()
    
    def test_get_student(self):
        id = self.db.getStudentId("John", "Doe")
        self.assertEqual(id, self.test_id)

    def test_getStudentGrade(self):
        grade = self.db.getStudentGrade(self.test_id)
        self.assertEqual(grade, 5)

    def test_addStudent(self):
        id = self.db.addStudent("james", 'cameron')
        test = self.db.cursor.execute("SELECT id FROM students where name = 'james' and lastname='cameron';").fetchone()[0]
        self.db.cursor.execute("DELETE FROM students where name = 'james' and lastname='cameron';")
        self.db._connection.commit()

        self.assertEqual(test, id)


if __name__ == '__main__': # точка входа в программу
   unittest.main(failfast=True)