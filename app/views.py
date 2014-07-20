from flask import jsonify
from app import app
from flask.ext import restful
from flask.ext.restful import reqparse
from flask.ext.login import LoginManager, login_user, login_required, logout_user, current_user, redirect
from flask import render_template, request
from search import SearchTags

import errors

from models import *


login_manager = LoginManager()
login_manager.init_app(app)

api = restful.Api(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


class Search(restful.Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, help='Search for any subject you need tutoring for.')
        parser.add_argument('price', type=int, help='What is the highest price you would pay? No cents to it!')
        parser.add_argument('lat', type=float, required=True, help="Need both GPS coordinates, latitude missing")
        parser.add_argument('lon', type=float, required=True, help="Need both GPS coordinates, longitude missing")
        parser.add_argument('radius', type=float, help="How far are you willing to travel")
        parser.add_argument('rating', type=float, help="What's the lowest rating you'd accept")
        args = parser.parse_args()

        query = args['query']
        max_price = args['price']
        user_gps = {'lat': args['lat'], 'lon': args['lon']}
        radius = args['radius']
        rating = args['rating']

        kwargs = dict(user_gps=user_gps)
        if radius:
            kwargs.update(radius=radius)

        if rating:
            kwargs.update(min_rating=rating)

        if query:
            kwargs.update(search_term=query)

        if max_price:
            kwargs.update(max_price=max_price)

        results = SearchTags().query(**kwargs)
        return restify(data=results)


api.add_resource(Search, '/api/search/')


class Ratings(restful.Resource):
    def get(self, tutor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, help='Rating of tutor')
        parser.add_argument('comment', type=str, help='Short review of tutor')
        parser.add_argument('user_id', type=int, help='User ID')
        args = parser.parse_args()
        try:
            user_id = args['user_id']
            rating = Rating.query.filter_by(user=user_id, tutor=tutor_id).first()
            if not rating:
                tutor = User.query.get(tutor_id)
                if not tutor:
                    return restify({"message": "Tutor_id does not exist"}, 400)
                rating = Rating(user=user_id, tutor=tutor_id, rating=int(args['rating']), comment=args['comment'])
                db.session.add(rating)
            else:
                rating.rating = int(args['rating'])

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return restify(data=e, status=500)

        return restify(data=args)

    @login_required
    def post(self, tutor_id):
        args = request.get_json(force=True)
        value =  args.get("rating")
        comment = args.get("comment")

        current_user_id = current_user.id

        try:
            newRating = Rating(user=current_user_id,
                               tutor=tutor_id,
                               rating=value,
                               comment=comment if comment else None)
            db.session.add(newRating)
            db.session.commit()
        except Exception as e:
            print "Couldn't add rating because %r" % e
            db.session.rollback()
            raise errors.InvalidUsage("Unable to add rating, sorry!")


api.add_resource(Ratings, '/api/rating/<int:tutor_id>')

class CreateAppointment(restful.Resource):
    def post(self, tutor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, help='Short message to send to tutor')
        parser.add_argument('subjects', type=str, help='String of subjects')
        parser.add_argument('user_id', type=int, help='User ID requesting the tutorings')
        args = parser.parse_args()
        try:
            user_id = args['user_id']
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

    @login_required
    def post(self):
        args = request.get_json(force=True)
        subject = args.get("subject") or args.get('tag') or args.get("name")
        if subject:
            try:
                new_tag = Tag(name=subject)
                db.session.add(new_tag)
                db.session.commit()
            except Exception as e:
                print "Couldn't add tag because %r" % e
                db.session.rollback()
                raise errors.SystemError("Unable to add subject, sorry!")
        else:
            raise errors.InvalidUsage("Please provide a subject")


api.add_resource(Subjects, '/api/subjects')

class Login(restful.Resource):
    def get(self, email):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='user email address')
        args = parser.parse_args()

api.add_resource(Login, '/api/login/<email>')




class UserProfile(restful.Resource):
    def get(self, user_id):
        try:
            user = User.query.get(user_id)
            appointments = Appointment.query.filter(db.or_(Appointment.user == user_id, Appointment.tutor == user_id)).order_by("created DESC")
            return restify(data={
                'user': user.serialize,
                'appointments': [appt.serialize for appt in appointments]
            })
        except Exception as e:
            return restify(data=e)


api.add_resource(UserProfile, '/api/profile/<int:user_id>')

class CreateInvoice(restful.Resource):
    def get(self, appointment_id, session_amount):
        parser = reqparse.RequestParser()
        parser.add_argument('appointment_id', type=str, help='user appointment id')
        parser.add_argument('session_amount', type=str, help='invoice ammount')

        appointments = Appointment.query.filter_by(id=appointment_id)
        appointments = [appt.serialize for appt in appointments]

        student_id = appointments[0]['student']['id']


        user_info = User.query.filter_by(id=student_id).first()
        user = user_info.serialize

        payment_id = user['payment']

        invoice = SimplifyProcessor()

        ret = invoice.create_invoice(payment_id, session_amount)

        app = Appointment.query.get(appointment_id)
        app.amount = session_amount
        app.invoice = ret['id']
        db.session.commit()


        return ret

api.add_resource(CreateInvoice, '/api/create_invoice/<int:appointment_id>/<int:session_amount>')

class LoginCat(restful.Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='user name', required=True)
        parser.add_argument('password', type=str, help='user password', required=True)
        args = parser.parse_args()

        username = args['username']
        password = args['password']



        cat = User.query.filter_by(username=username).all()[0]
        print "Found user : %r" % cat
        if cat and cat.password == password:
            login_user(cat)
        else:
            raise errors.Permission("Incorrect username or password")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='user name', required=True)
        parser.add_argument('password', type=str, help='user password', required=True)
        args = parser.parse_args()

        username = args['username']
        password = args['password']



        cat = User.query.filter_by(username=username).all()[0]
        print "Found user : %r" % cat
        if cat and cat.password == password:
            login_user(cat)
        else:
            raise errors.Permission("Incorrect username or password")

api.add_resource(LoginCat, '/api/login')



@app.route('/api/logout', methods=['GET', 'POST'])
@login_required
def logout_cat():
    message = "Good Bye " + current_user.name  + ", come again!"
    print message
    logout_user()
    return redirect("http://college.cat")

# Errors
@app.errorhandler(401)
def handler_unauthorized(error):
    response, code = restify(error)
    return jsonify(response), code

@app.errorhandler(errors.SystemError)
def handle_system_error(error):
    return restify(error)


@app.errorhandler(errors.InvalidUsage)
def handle_invalid_usage(error):
    return restify(error)

@app.errorhandler(errors.Permission)
def handle_permission(error):
    return restify(error)

def restify(data, status=None):
    if isinstance(data, Exception):
        try:
            status = int(status or data.status_code)
        except:
            try:
                status = int(data.code or 500)
            except:
                status = 500

        data = {'exception': data.message or str(data)}

    elif isinstance(data, (list, dict)):
        status = int(status or 200)

    else:
        raise errors.SystemError("Restify wasn't given correct params")

    return {'data': data or {},
            'status': status}, status


@app.route('/find_invoice/<invoice_id>')
def find_invoice(invoice_id):
    invoice = SimplifyProcessor()
    print invoice.find_invoices(invoice_id)

@app.route('/create_invoice/<user_id>/<int:amount>')
def create_invoice(user_id, amount):
    invoice = SimplifyProcessor()

    print invoice.create_invoice(user_id, amount)
