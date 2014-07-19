from flask import jsonify
from app import app
from flask.ext import restful

api = restful.Api(app)


class HelloWorld(restful.Resource):
    def get(self):
        return jsonify(data="Hello World")

api.add_resource(HelloWorld, '/')