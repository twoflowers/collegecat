from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class CloudForm(Form):

    hostname = TextField('hostname', validators = [Required()])
    email = TextField('email', validators = [Required()])
