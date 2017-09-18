from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key="nitin"
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []

class ListItems(Resource):
    def get(self):
        return {"items":items}

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
    type = float,
    required = True,
    help = "price field can't be empty!!"
    )
    @jwt_required()
    def get(self,name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item":item},202 if item else 404

    def post(self,name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item != None:
            return {"messeage": "{} is already present please try another".format(name)},400
        data = Items.parser.parse_args()
        item = {"name": name , "price": data["price"]}
        items.append(item)
        return item,201

    def delete(self,name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item deleted successfully!!"}

    def put(self,name):
        data = Items.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items),None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item
api.add_resource(ListItems, "/items")
api.add_resource(Items, "/item/<string:name>")
api.add_resource(UserRegister, "/register")

app.run(port = 5000, debug = True)
