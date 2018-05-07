from flask import Flask
from flask_restful import  Api, output_json
from flask_jwt import JWT
from flask_cors import CORS
from item import Item, ItemList
from itemDetail import ItemDetail
from tag import TagsList
from security import authenticate, identity

app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.config['RESTFUL_JSON'] = { 'ensure_ascii': False } #To allow all responses unicode. 
representations = {
            'application/json; charset=utf-8': output_json,
        }
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(ItemDetail, '/item/<int:id>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(TagsList, '/tags')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True


# endpoint to get user detail by id

