import sqlite3 
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from tag import Tag

class Item(Resource):
    parser = reqparse.RequestParser()
    price = parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    description = parser.add_argument('description', type=str, required =True, help="This field cannot be left blank!")

    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'},404
    
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

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor() 

        query = "SELECT * FROM items WHERE NAME=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row: 
            return {'item': {'id':row[0], 'name':row[1], 'price':row[2],'description': row[3]}}
        
    
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.price.parse_args()
        data = Item.description.parse_args()
        tag = Tag.tag.parse_args()

        item = {'name': name, 'price': data['price'], 'description': data['description']}
        tag =  {'tag': tag['tag']}
        
        if ',' in tag['tag']:
            tags_list = tag['tag'].split(',')
            for tag in tags_list:
                str_tag = ''.join(tag)
                self.insert(item,str_tag)
        else:
            self.insert(item,tag)

        
        # try:
        #     self.insert(item)
        # except:
        #     return {"message": "An error occured inserting data"}, 500

        return item,201
        

    @classmethod
    def insert(cls,item,tag):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        str_tag = ''.join(tag)

        if not cls.find_by_name(item['name']):
            query = "INSERT INTO items(name,price,description) VALUES (?,?,?)"
            cursor.execute(query, (item['name'],item['price'], item['description']))
        
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

    # @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close() 
        return {'message': 'Item deleted'}

    # @jwt_required()
    # def put(self, name):
    #     data = Item.parser.parse_args()
        
    #     item = self.find_by_name(name)
    #     updated_item = {'name': name, 'price': data['price'], 'description':data['description']}

    #     if item is None:
    #         try:
    #             self.insert(updated_item)
    #         except:
    #             return {"message": "An error occured on the insert method "},500
    #     else:
    #         try:
    #             self.update(updated_item)
    #         except:
    #             return {"message": "An error occured on the update method"}, 500
    #     return updated_item

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name'], item['description']))

        connection.commit()
        connection.close() 

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items" 
        result = cursor.execute(query)
        items = []

        for row in result: 
            items.append({ 'id':row[0], 'name': row[1], 'price': row[2], 'description':row[3]})

        connection.close() 

        return{'items':items}

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