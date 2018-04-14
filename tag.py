import sqlite3 
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

class Tag(Resource):
    parser = reqparse.RequestParser()
    tag = parser.add_argument('tag', type=str, required = True, help="This field cannot be left blank")

