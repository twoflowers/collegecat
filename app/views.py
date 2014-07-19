from flask import render_template, flash, redirect, request
from app import app
from forms import LoginForm
from models import codero_api

api = codero_api()


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    servers = api.list_running()
    return render_template('cloud.html', title='One Hour Cloud', running = servers)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/cloud', methods=['POST'])
def cloud():
    hostname = request.form['hostname']
    email = request.form['email']

    create_vm(hostname, email)

    return redirect('/')

@app.route('/delete/<vm_id>', methods=['GET'])
def delete(vm_id):

    api.delete_vm(vm_id)
    return redirect('/')


def create_vm(hostname, email):
    print 'creating vm'
    api.create_vm(hostname, email)
