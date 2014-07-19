import requests, json
from app import app

class codero_api():
    def __init__(self):
        self.api_key = app.config['CODERO_API_KEY']
        self.url = app.config['CODERO_API_URL']

    def api_request(self, command, request_type = 'GET', data=''):
        if request_type == 'POST':

            return requests.post("%s%s" % (self.url, command),data=json.dumps(data),headers={'Authorization':'%s' % self.api_key, 'Content-Type':'application/json'})
        elif request_type == 'DELETE':
            return requests.delete("%s%s/%s" % (self.url, command, data), headers={'Authorization': '%s' % self.api_key})
        else:
            return requests.get("%s%s" % (self.url, command), headers={'Authorization': '%s' % self.api_key})


    def list_running(self):
        return self.api_request('servers').json()

    def create_vm(self, hostname, email):
        data = {
            'name': hostname,
            'codelet': app.config['CODERO_API_CODELET'],
            'billing': app.config['CODERO_API_BILLING_TYPE']
        }
        self.api_request('servers', 'POST', data)

    def delete_vm(self, vm_id):
        self.api_request('servers', 'DELETE', vm_id)
