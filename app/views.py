from flask import jsonify
from app import app
from flask.ext import restful
from flask import render_template

api = restful.Api(app)


class HelloWorld(restful.Resource):
    def get(self):
        return jsonify(data="Hello World")

api.add_resource(HelloWorld, '/api/')

@app.route('/')
def index():
    return render_template('base.html')

