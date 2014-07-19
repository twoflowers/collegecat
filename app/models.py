# Built In
import datetime

# Module
from app import app

# 3rd Party
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


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