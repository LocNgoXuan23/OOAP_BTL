import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1234',
    database ='tkhdt_project'
)

mycursor = db.cursor()

if __name__ == '__main__':
    # create table
    mycursor.execute("CREATE TABLE Users (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, created datetime NOT NULL, username VARCHAR(50) NOT NULL, passwd VARCHAR(50) NOT NULL, role ENUM('0', '1', '2', '3') NOT NULL, name VARCHAR(50) NOT NULL DEFAULT 'none', gender ENUM('M', 'F', 'O') NOT NULL DEFAULT 'O', addr VARCHAR(50) NOT NULL DEFAULT 'none', phone VARCHAR(50) NOT NULL DEFAULT 'none', email VARCHAR(50) NOT NULL DEFAULT 'none')")
    mycursor.execute("CREATE TABLE Students (id int PRIMARY KEY NOT NULL, created datetime NOT NULL, grade VARCHAR(50) NOT NULL DEFAULT 'none', classId int NOT NULL DEFAULT -1, schoolYear int NOT NULL DEFAULT -1, IdNumber int NOT NULL DEFAULT -1)")
    mycursor.execute("CREATE TABLE Managers (id int PRIMARY KEY NOT NULL, created datetime NOT NULL, IdNumber int NOT NULL DEFAULT -1)")
    mycursor.execute("CREATE TABLE Teachers (id int PRIMARY KEY NOT NULL, created datetime NOT NULL, IdNumber int NOT NULL DEFAULT -1)")
    mycursor.execute("CREATE TABLE Classes (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, created datetime NOT NULL, className VARCHAR(50) NOT NULL, teacherId int DEFAULT -1)")
    mycursor.execute("CREATE TABLE SubjectClasses (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, created datetime NOT NULL, subjectName VARCHAR(50) NOT NULL, teacherId int DEFAULT -1)")
    mycursor.execute("CREATE TABLE Scores (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, created datetime NOT NULL, subjectClassId int NOT NULL DEFAULT -1, studentId int NOT NULL DEFAULT -1, score int NOT NULL DEFAULT -1)")

    mycursor.execute("ALTER TABLE Teachers ADD COLUMN type ENUM('0', '1') NOT NULL DEFAULT '0', ADD COLUMN classId int NOT NULL DEFAULT -1, ADD COLUMN subjectClassIds VARCHAR(50) DEFAULT '[]'")
    mycursor.execute("ALTER TABLE SubjectClasses ADD COLUMN classId int NOT NULL DEFAULT -1")
    mycursor.execute("ALTER TABLE Students ADD COLUMN classId int NOT NULL DEFAULT -1")
    mycursor.execute("ALTER TABLE Students ADD COLUMN classId int NOT NULL DEFAULT -1")

    mycursor.execute("ALTER TABLE Teachers MODIFY COLUMN subjectClassIds VARCHAR(50) DEFAULT ''")

    # mycursor.execute("DROP TABLE Classes")
    # mycursor.execute("DROP TABLE SubjectClasses")

    # mycursor.execute("DESCRIBE Teachers")
    mycursor.execute("SHOW TABLES")

    for x in mycursor:
        print(x)

    # mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s,%s,%s)", ("Long", datetime.now(), "F"))
    