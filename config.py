
simplify_public_key = "sbpb_MWJlOWRjZGEtZWUyMC00NDAzLWI4MGYtMTQ3N2ZiOWE1ODY4"
simplify_private_key = "poST9vBz/bxRCL5sye6xVpssOZFOLntt2ZUEEzPHig55YFFQL0ODSXAOkNtXTToq"
simplify_reference = ""

sendgrid_username = 'collegecat'
sendgrid_password = '7HsCLiiL'

SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

db_host = 'localhost'
db_user = 'collegecat'
db_pass = 'UrNotAG04t'
db_name = 'collegecat'


SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{psw}@{host}/{name}'.format(user=db_user, host=db_host,
                                                                      psw=db_pass, name=db_name)

college_cat_email = """
Hello,

We are informing you that %s is looking for a tutor and has requested a meetup time with you in the subject of
%s.

Contact Information for %s :

Email: %s
Phone: %s
"""