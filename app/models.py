from app import app
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

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    # department = db.Column(db.ForeignKey())

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    payment = db.Column(db.String(100), )
    name = db.Column(db.String(80), unique=True)
    bio = db.Column(db.String(1000), nullable=True)
    loc = db.Column(db.ForeignKey(Location.id))
    # subjects =

    def __init__(self, username, password, email, payment, name):
        self.username = username
        self.password = password
        self.email = email
        self.payment = payment
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.username

# class codero_api():
#     def __init__(self):
#         self.api_key = app.config['CODERO_API_KEY']
#         self.url = app.config['CODERO_API_URL']
#
#     def api_request(self, command, request_type = 'GET', data=''):
#         if request_type == 'POST':
#
#             return requests.post("%s%s" % (self.url, command),data=json.dumps(data),headers={'Authorization':'%s' % self.api_key, 'Content-Type':'application/json'})
#         elif request_type == 'DELETE':
#             return requests.delete("%s%s/%s" % (self.url, command, data), headers={'Authorization': '%s' % self.api_key})
#         else:
#             return requests.get("%s%s" % (self.url, command), headers={'Authorization': '%s' % self.api_key})
#
#
#     def list_running(self):
#         return self.api_request('servers').json()
#
#     def create_vm(self, hostname, email):
#         data = {
#             'name': hostname,
#             'codelet': app.config['CODERO_API_CODELET'],
#             'billing': app.config['CODERO_API_BILLING_TYPE']
#         }
#         self.api_request('servers', 'POST', data)
#
#     def delete_vm(self, vm_id):
#         self.api_request('servers', 'DELETE', vm_id)
