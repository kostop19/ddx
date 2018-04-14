import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_items_table = "CREATE TABLE IF NOT EXISTS items(Id integer primary key autoincrement, name text, price real, description text);"
create_tags_table = "CREATE TABLE IF NOT EXISTS tags(Id integer primary key autoincrement,tag text);"
create_items_tags_table="CREATE TABLE IF NOT EXISTS tagitems(ItemId integer,TagId integer);"

cursor.execute(create_items_table)
cursor.execute(create_items_tags_table)

query = "INSERT INTO items(name,price,description) VALUES (?,?,?)"
cursor.execute(query, ('GUITAR',22, 'This is a description'))
cursor.execute(query, ('PIANO',24, 'This is a description'))
cursor.execute(query, ('TABLE',22, 'This is a description'))
cursor.execute(query, ('WINDOW',24, 'This is a description'))

cursor.execute(create_tags_table)

tagsquery = "INSERT INTO tags(tag) VALUES (?)"
cursor.execute(tagsquery,('musical instrument',)) 
cursor.execute(tagsquery,('Home',)) 
cursor.execute(tagsquery,('Guitar',)) 
cursor.execute(tagsquery,('Table',)) 
cursor.execute(tagsquery,('Chair',)) 

connection.commit()
connection.close()