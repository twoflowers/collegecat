from flask import jsonify
from app import app
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import render_template

api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return jsonify(data="Hello World")


api.add_resource(HelloWorld, '/api/')


class Ratings(restful.Resource):
    def get(self, tutor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, help='Rating of tutor')
        args = parser.parse_args()
        return jsonify(data=args)

api.add_resource(Ratings, '/api/rating/<int:tutor_id>')


@app.route('/')
def index():
    return render_template('base.html')


def restify(data, status=200):
    status = int(status)
    return {'data': data,
            'status': status}, status
