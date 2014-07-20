from flask import jsonify
from app import app
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import render_template
import errors

from models import *

api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        return restify(data="Hello World")


api.add_resource(HelloWorld, '/api/')


class Ratings(restful.Resource):
    def get(self, tutor_id):
        # TODO: Find logged-in user
        user_id = 300
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, help='Rating of tutor')
        parser.add_argument('comment', type=str, help='Short review of tutor')
        args = parser.parse_args()
        try:
            rating = Rating.query.filter_by(user=user_id, tutor=tutor_id).first()
            if not rating:
                tutor = User.query.get(tutor_id)
                if not tutor:
                    return restify({"message": "Tutor_id does not exist"}, 400)
                rating = Rating(user=user_id,tutor=tutor_id,rating=int(args['rating']),comment=args['comment'])
                db.session.add(rating)
            else:
                rating.rating = int(args['rating'])

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return restify(data=e, status=500)

        return restify(data=args)

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
        try:
            status = int(status or data.status_code or 500)
        except:
            status = 500

        data = {'exception': data.message}

    elif isinstance(data, (list, dict)):
        status = int(status or 200)

    else:
        raise errors.SystemError("Restify")

    return {'data': data,
            'status': status}, status


@app.route('/find_invoice/<invoice_id>')
def find_invoice(invoice_id):
    invoice = SimplifyProcessor()
    print invoice.find_invoices(invoice_id)

@app.route('/create_invoice/<user_id>/<int:amount>')
def create_invoice(user_id, amount):
    invoice = SimplifyProcessor()

    print invoice.create_invoice(user_id, amount)
