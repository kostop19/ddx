import sqlite3 
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
from tag import Tag
from medicine import Medicine
class Item(Resource):
    parser = reqparse.RequestParser()
    risk_factors = parser.add_argument('risk_factors', type=str, required =True, help="This field cannot be left blank!")
    laboratory = parser.add_argument('laboratory', type=str, required =True, help="This field cannot be left blank!")
    tests = parser.add_argument('tests', type=str, required =True, help="This field cannot be left blank!")
    illustration = parser.add_argument('illustration', type=str, required =True, help="This field cannot be left blank!")
    

    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'},404
    
   
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
            items.append({ 'id':row[0], 'name':row[1], 'risk_factors':row[2],'laboratory': row[3], 'tests': row[4], 'illustration':row[5]})

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