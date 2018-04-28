import sqlite3 
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

class Medicine(Resource):
    parser = reqparse.RequestParser()
    medicine = parser.add_argument('medicine', type=str, required = True, help="This field cannot be left blank")

    @classmethod
    def parse_field(cls,field):
        field_str = list(field.values())
        print(field_str)
        if ',' in field_str[0]:
            fields_list = field_str[0].split(',')
            for field in fields_list:
                str_field = ''.join(field)
                cls.insert_medicine(str_field)
        else:
            str_field = ''.join(field_str)
            cls.insert_medicine(field_str)

    @classmethod
    def insert_medicine(cls,field):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        str_medicine = ''.join(field)

        if cls.find_by_field(str_medicine):
           findId = """INSERT INTO medicineitems (itemid,medicineid) SELECT items.Id, medicines.id FROM ITEMS, tags 
           WHERE medicines.ID = (SELECT MAX(ID) FROM ITEMS) and medicines.medicine = ?;"""

           cursor.execute(findId, (str_medicine,))
        else:
            insertField = "INSERT INTO medicines(medicine) VALUES(?)"
            cursor.execute(insertField, (str_medicine,))
            findId = """INSERT INTO medicineitems (itemid,medicineid) SELECT items.Id, medicines.id FROM ITEMS, medicines 
            WHERE items.ID = (SELECT MAX(ID) FROM ITEMS) and medicines.medicine = ?;"""

            cursor.execute(findId, (str_medicine,))

        connection.commit()
        connection.close()

    @classmethod
    def find_by_field(cls,medicine):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM MEDICINES WHERE MEDICINE=?"
        str_medicine = ''.join(medicine)
        result = cursor.execute(query,(str_medicine,))
        row = result.fetchone()
        connection.close()

        if row: 
            return {'medicine': {'id':row[0], 'medicine':row[1]}}
            
class MedicinesList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM medicines"
        result = cursor.execute(query)
        medicines = []

        for row in result:
            medicines.append({'id':row[0],'tag':row[1]})
        
        connection.close()

        return{'medicines':medicines}
