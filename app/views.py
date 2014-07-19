from app import app
from flask.ext import restful

api = restful.Api(app)


class HelloWorld(restful.Resource):
    def get(self):
        return restify("blah")

api.add_resource(HelloWorld, '/api')


def restify(data, status=200):
    status = int(status)
    return {'data':data,'status':status}, status


