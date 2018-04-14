from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from flask_cors import CORS
from item import Item, ItemList, TagsList

from security import authenticate, identity

app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(TagsList, '/tags')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
