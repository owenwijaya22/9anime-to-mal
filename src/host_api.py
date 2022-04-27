from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)



class Apis(Resource):
    def get(self):
        access_token = request.args.get('code')
        return {"copy this value": access_token}


api.add_resource(Apis, "/get")

if __name__ == "__main__":
    app.run(debug=True)