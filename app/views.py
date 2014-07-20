from flask import jsonify
from app import app
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import render_template
import errors

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


# Errors
@app.errorhandler(errors.SystemError)
def handle_system_error(error):
    return restify(error)


@app.errorhandler(errors.InvalidUsage)
def handle_invalid_usage(error):
    return restify(error)


def restify(data, status=None):

    if isinstance(data, Exception):
        status = int(status) or data.status_code or 500
        data = {'exception': data.message}

    elif isinstance(data, (list, dict)):
        status = int(status) or 200

    else:
        raise errors.SystemError("Restify")

    return {'data': data,
            'status': status}, status
