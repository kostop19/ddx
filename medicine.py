import sqlite3 
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

class Medicine(Resource):
    parser = reqparse.RequestParser()
    medicine = parser.add_argument('medicine', type=str, required = True, help="This field cannot be left blank")

