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

class CreateAppointment(restful.Resource):
    def post(self, tutor_id):
        # TODO: Find logged-in user
        user_id = 300
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, help='Short message to send to tutor')
        parser.add_argument('subjects', type=str, help='String of subjects')
        args = parser.parse_args()
        try:
            tutor = User.query.get(tutor_id)
            user = User.query.get(user_id)
        except Exception as e:
            return restify(e)

        try:
            newAppt = Appointment(user_id, tutor_id, args['message'])
            db.session.add(newAppt)
            db.session.commit()
            sp = SendgridProcessor()
            sp.send(to=tutor.email, student_name=user.name,
                    tutor_subject=args['subjects'],
                    student_email=user.email,
                    student_phone=user.phone,
                    user_message=args['message'])
            return restify(data={"message": "Notification sent successfully!"})
        except Exception as e:
            db.session.rollback()
            return restify(data={"exception": "%r" % e}, status=500)


class DeleteAppointment(restful.Resource):
    def get(self, appointment_id):
        try:
            appt = Appointment.query.get(appointment_id)
            db.session.delete(appt)
            db.session.commit()
            return restify(data={"message": "Appointment ID %s deleted." % appointment_id})
        except Exception as e:
            db.session.rollback()
            return restify(data={"exception": "%r" % e}, status=500)

api.add_resource(DeleteAppointment, '/api/delete_appointment/<int:appointment_id>')
api.add_resource(CreateAppointment, '/api/create_appointment/<int:tutor_id>')


class Subjects(restful.Resource):
    def get(self):
        return [tag.serialize for tag in db.session.query(Tag).all()]

api.add_resource(Subjects, '/api/subjects')

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
