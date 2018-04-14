import sqlite3 

connection = sqlite3.connect('students.db')
cursor = connection.cursor()

create_student_table = "CREATE TABLE students (ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL);"
create_course_table = "CREATE TABLE courses (ID INT PRIMARY KEY NOT NULL, LESSON TEXT NOT NULL);"           
create_studentCourses_table = "CREATE TABLE studentcourses(STUDENT_ID INT, COURSE_ID);"
           
cursor.execute(create_student_table)
cursor.execute(create_course_table)
cursor.execute(create_studentCourses_table)

connection.commit()
connection.close()