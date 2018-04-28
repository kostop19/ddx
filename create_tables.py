import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# create_items_table = "CREATE TABLE IF NOT EXISTS items(Id integer primary key autoincrement, name text, price real, description text);"
create_disease_table = "CREATE TABLE IF NOT EXISTS items(Id integer primary key autoincrement, name text, risk_factors text, laboratory text, illustration text, tests text);"
create_tags_table = "CREATE TABLE IF NOT EXISTS tags(Id integer primary key autoincrement,tag text);"
create_items_tags_table="CREATE TABLE IF NOT EXISTS tagitems(ItemId integer,TagId integer);"
create_medicines_table="CREATE TABLE IF NOT EXISTS medicines(Id integer primary key autoincrement,medicine text)"
create_items_medicines_table="CREATE TABLE IF NOT EXISTS medicineitems(ItemId integer,MedicineId integer);"

# cursor.execute(create_items_table)
cursor.execute(create_disease_table)
cursor.execute(create_items_tags_table)
cursor.execute(create_tags_table)
cursor.execute(create_medicines_table)
cursor.execute(create_items_medicines_table)
# query = "INSERT INTO items(name,price,description) VALUES (?,?,?)"
# cursor.execute(query, ('GUITAR',22, 'This is a description'))
# cursor.execute(query, ('PIANO',24, 'This is a description'))
# cursor.execute(query, ('TABLE',22, 'This is a description'))
# cursor.execute(query, ('WINDOW',24, 'This is a description'))

# cursor.execute(create_tags_table)

# tagsquery = "INSERT INTO tags(tag) VALUES (?)"
# cursor.execute(tagsquery,('musical instrument',)) 
# cursor.execute(tagsquery,('Home',)) 
# cursor.execute(tagsquery,('Guitar',)) 
# cursor.execute(tagsquery,('Table',)) 
# cursor.execute(tagsquery,('Chair',)) 


#SELECT NAME,  LESSON FROM STUDENTS JOIN studentcourses ON STUDENTS.ID = studentcourses.STUDENT_ID 
#JOIN COURSES ON studentcourses.COURSE_ID = courses.ID 
#WHERE LESSON = "Javascript";

connection.commit()
connection.close()