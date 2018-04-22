import sqlite3 
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

class Tag(Resource):
    parser = reqparse.RequestParser()
    tag = parser.add_argument('tag', type=str, required = True, help="This field cannot be left blank")

    @classmethod
    def parse_field(cls,field):
        field_str = list(field.values())
        print(field_str)
        if ',' in field_str[0]:
            fields_list = field_str[0].split(',')
            for field in fields_list:
                str_field = ''.join(field)
                cls.insert_tag(str_field)
        else:
            str_field = ''.join(field_str)
            cls.insert_tag(field_str)

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

class TagsList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM tags"
        result = cursor.execute(query)
        tags = []

        for row in result:
            tags.append({'id':row[0],'tag':row[1]})
        
        connection.close()

        return{'tags':tags}