import sqlite3

class DB:
    def __init__(self, path: str):
        self._connection =  sqlite3.connect(path)

    @property
    def cursor(self):
        return self.__cursor
    
    @cursor.getter
    def cursor(self):
        return self.__cursor
    
    def newCursor(self):
        self.__cursor = self._connection.cursor()
    
    def closeCursor(self):
        self.__cursor.close()

    def getStudentId(self, name, lastname: str) -> int:
        self.cursor.execute('SELECT id FROM students WHERE name = :name and lastname = :lastname',
            {"name": name, "lastname": lastname})
    
        return self.cursor.fetchone()[0]

    def getStudentGrade(self, id: int) -> int:
        self.cursor.execute('SELECT grade FROM grades WHERE student_id= ?', (id,))
        return self.cursor.fetchone()[0]

    def addStudent(self, name, lastname: str) -> int:
        self.cursor.execute("INSERT INTO students(name, lastname) VALUES (?, ?);",
            (name, lastname))
        self._connection.commit()
        return self.__cursor.lastrowid

path = "../testrepo/testrepo/db/testdb.db"