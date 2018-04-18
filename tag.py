import sqlite3 
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

class Tag(Resource):
    parser = reqparse.RequestParser()
    tag = parser.add_argument('tag', type=str, required = True, help="This field cannot be left blank")

    @classmethod
    def insert_tag(cls,tag):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        str_tag = ''.join(tag)

        if cls.find_by_tag(str_tag):
           findId = """INSERT INTO tagitems (itemid,tagid) SELECT items.Id, tags.id FROM ITEMS, tags 
           WHERE items.ID = (SELECT MAX(ID) FROM ITEMS) and tags.tag = ?;"""

           cursor.execute(findId, (str_tag,))
        else:
            insertTag = "INSERT INTO tags(tag) VALUES(?)"
            cursor.execute(insertTag, (str_tag,))
            findId = """INSERT INTO tagitems (itemid,tagid) SELECT items.Id, tags.id FROM ITEMS, tags 
            WHERE items.ID = (SELECT MAX(ID) FROM ITEMS) and tags.tag = ?;"""

            cursor.execute(findId, (str_tag,))

        connection.commit()
        connection.close()

    @classmethod
    def find_by_tag(cls,tag):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM tags WHERE TAG=?"
        str_tag = ''.join(tag)
        result = cursor.execute(query,(str_tag,))
        row = result.fetchone()
        connection.close()

        if row: 
            return {'tag': {'id':row[0], 'tag':row[1]}}

