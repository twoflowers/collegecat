# Built In
import datetime

# Module
from app import app

# 3rd Party
from flask.ext.sqlalchemy import SQLAlchemy
import requests

db = SQLAlchemy(app)


class simplify(object):
    def __init__(self):

        simplify.public_key = app.config['simplify_public_key']
        simplify.private_key = app.config['simplify_private_key']

    def make_payment(self, cc_number, cc_exp_month, cc_exp_year, cc_cvc, amount, description):
        try:
            payment = simplify.Payment.create({
               "card" : {
                    "number": "%s" % cc_number,
                    "expMonth": cc_exp_month,
                    "expYear": cc_exp_year,
                    "cvc": "%s" % cc_cvc
                },
                "amount" : "%s" % amount,
                "description" : "%s" % description,
                "currency" : "USD"
            })
        except:
            return payment.paymentStatus


        if payment.paymentStatus == 'APPROVED':
            return True

    def create_user(self):
        user = simplify.Customer.create({
            "email" : "customer@mastercard.com",
            "name" : "Customer Customer",
            "card" : {
               "expMonth" : "11",
               "expYear" : "19",
               "cvc" : "123",
               "number" : "5555555555554444"
            },
            "reference" : "Ref1"})

        return user

    def find_user(self, info):
        user = simplify.Customer.find('%s') % info

        return user

    def delete_user(self, info):
        user = self.find_user(info)

        user.delete()

    def update_user(self, key, value, info):
        # @todo not needed for this hack
        return True


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip = db.Column(db.String(10), nullable=True)
    gps = db.Column(db.String(100), unique=True)

    def __init__(self, street, city, state, zip, gps):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.gps = gps

    def __repr__(self):
        return '<Location {city}, {state} {zip} (gps:{gps})>'.format(city=self.city, state=self.city,
                                                                     zip=zip, gps=self.gps)
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Department %r>' % self.name



class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    course_number = db.Column(db.String(100), nullable=True)
    department = db.Column(db.ForeignKey(Department.id), nullable=True)

    def __init__(self, name, department):
        self.name = name
        self.department = department

    def __repr__(self):
        return '<Subject %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    payment = db.Column(db.String(100), )
    name = db.Column(db.String(80), unique=True)
    bio = db.Column(db.String(1000), nullable=True)
    loc = db.Column(db.Integer, db.ForeignKey(Location.id))
    subjects = db.relationship('Subject', backref='user', lazy='dynamic')
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password, email, payment, name):
        self.username = username
        self.password = password
        self.email = email
        self.payment = payment
        self.name = name

    def __repr__(self):
        return '<User {name}({username}) email: {email} /' \
               'subjects: {subjects}>'.format(name=self.name, email=self.email,
                                              username=self.username, subjects=len(self.subjects))


class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('Subject', backref='user', lazy='dynamic')


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    tutor = db.Column(db.Integer, db.ForeignKey(Tutor.id))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(1000), nullable=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, tutor, rating, comment):
        if user is not tutor:
            self.user = user
            self.tutor = tutor
            self.rating = rating
            self.comment = comment
        else:
            raise RuntimeError("Auto-rating prohibited")

    def __repr__(self):
        return "<Rating {rating} : {comment}>".format(rating=self.rating,
                                                      comment="" if not self.comment else self.comment)


class pipl(object):
    def __init__(self):
        self.pipl_api_key = app.config['pipl_key']
        self.pipl_api_url = app.config['pipl_key']

    def search (self, user_id, first_name, last_name, email_address):
        # @todo update user table with information
        # @todo clean up the return value
        url = "%sfirst_name=%s&last_name=%s&email=%s&key=%s&pretty=true" % (
            self.pipl_api_url,
            first_name,
            last_name,
            email_address,
            self.pipl_api_key)

        req = requests.get(url)

        return req.json()