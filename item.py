import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
from tag import Tag
from medicine import Medicine


class Item(Resource):
    parser = reqparse.RequestParser()
    risk_factors = parser.add_argument(
        'risk_factors', type=str, required=True, help="This field cannot be left blank!")
    laboratory = parser.add_argument(
        'laboratory', type=str, required=True, help="This field cannot be left blank!")
    tests = parser.add_argument(
        'tests', type=str, required=True, help="This field cannot be left blank!")
    illustration = parser.add_argument(
        'illustration', type=str, required=True, help="This field cannot be left blank!")

    # @jwt_required()

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor() 

        query = "SELECT * FROM items WHERE NAME=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row: 
            return {'item': {'id':row[0], 'name':row[1], 'risk_factors':row[2],'laboratory': row[3], 'tests': row[4], 'illustration':row[5]}}
        
    

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.risk_factors.parse_args()
        data = Item.laboratory.parse_args()
        data = Item.tests.parse_args()
        data = Item.illustration.parse_args()

        tag = Tag.tag.parse_args()
        medicine = Medicine.medicine.parse_args()

        item = {'name': name,'risk_factors': data['risk_factors'], 'laboratory':data['laboratory'],'tests':data['tests'],  'illustration': data['illustration']}
        tag =  {'tag': tag['tag']}
        medicine = {'medicine':medicine['medicine']}

        self.insert(item)

        Tag.parse_field(tag)
        Medicine.parse_field(medicine)

        return item,201
        

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()


        if not cls.find_by_name(item['name']):
            query = "INSERT INTO items(name, risk_factors, laboratory, illustration, tests) VALUES (?,?,?,?,?)"
            cursor.execute(query, (item['name'],item['risk_factors'], item['laboratory'], item['illustration'],item['tests']))

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
            items.append({ 'id':row[0], 'name':row[1], 'risk_factors':row[2],'laboratory': row[3], 'tests': row[4], 'illustration':row[5]})

        connection.close() 

        return{'items':items}


class ItemDetail(Resource):
    parser = reqparse.RequestParser()
    name = parser.add_argument(
        'name', type=str, required=True, help="This field cannot be left blank!")
    risk_factors = parser.add_argument(
        'risk_factors', type=str, required=True, help="This field cannot be left blank!")
    laboratory = parser.add_argument(
        'laboratory', type=str, required=True, help="This field cannot be left blank!")
    tests = parser.add_argument(
        'tests', type=str, required=True, help="This field cannot be left blank!")
    illustration = parser.add_argument(
        'illustration', type=str, required=True, help="This field cannot be left blank!")

    def get(self, id):
        item = self.find_by_id(id)
        tags = self.find_tags_by_id(id)
        Item = []

        Item.append(item)
        Item.append(tags)

        if item:
            return Item
        return {'message': 'Item not found'}, 404
        
    # @jwt_required()
    def delete(self, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        item = "DELETE FROM items WHERE ID = ?"
        tags = "DELETE FROM tagitems where ItemId = ?"
        
        cursor.execute(item, (id,))
        cursor.execute(tags,(id,))

        connection.commit()
        connection.close() 
        return {'message': 'Item deleted'}

     # @jwt_required()
    def put(self, id):
        data = ItemDetail.parser.parse_args()

        print(data)
        item = self.find_by_id(id)
        updated_item = {'id': id,'name':data['name'] ,'risk_factors': data['risk_factors'], 'laboratory':data['laboratory'],'tests':data['tests'], 'illustration': data['illustration']}

        if item:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occured on the insert method "},500
        return updated_item

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET risk_factors=?, laboratory=?, illustration=?, tests=?, name=? WHERE ID=?"
        cursor.execute(query, (item['risk_factors'], item['laboratory'], item['illustration'],item['tests'],item['name'],item['id']))

        connection.commit()
        connection.close() 

    @classmethod
    def find_by_id(cls,id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor() 

        query = "SELECT * FROM items WHERE ID=?"

        result = cursor.execute(query,(id,))
       
        row = result.fetchone()
       
        connection.close()

        if row: 
            return {'item': {'id':row[0], 'name':row[1], 'risk_factors':row[2],'laboratory': row[3], 'tests': row[4], 'illustration':row[5] }}
    
    @classmethod
    def find_tags_by_id(cls,id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT tag FROM items JOIN tagitems ON items.id = tagitems.itemid 
                      JOIN tags ON tagitems.tagid = tags.ID 
                      WHERE items.id = ?;"""

        result = cursor.execute(query,(id,))
        rows = result.fetchall()

        connection.close()

        tags = []

        for row in rows:
            tags.append({'tag':row[0]})

        Tags = {'tags':tags}

        return Tags

    
           
            