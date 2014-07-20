
simplify_public_key = "sbpb_MWJlOWRjZGEtZWUyMC00NDAzLWI4MGYtMTQ3N2ZiOWE1ODY4"
simplify_private_key = "poST9vBz/bxRCL5sye6xVpssOZFOLntt2ZUEEzPHig55YFFQL0ODSXAOkNtXTToq"
simplify_reference = ""

SENDGRID_USERNAME = 'collegecat'
SENDGRID_PASSWORD = '7HsCLiiL'

SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

db_host = 'localhost'
db_user = 'collegecat'
db_pass = 'UrNotAG04t'
db_name = 'collegecat'


SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{psw}@{host}/{name}'.format(user=db_user, host=db_host,
                                                                      psw=db_pass, name=db_name)

COLLEGE_CAT_EMAIL = """
Hello,
<br>
<p>We are informing you that %s is looking for a tutor and has requested a meetup with you in the subject of
%s.</p>
<br>
<br>Contact Information for %s :
<br>
<br><strong>Email</strong>: %s
<br><strong>Phone</strong>: %s
<br>
<br>The message they left is:
<p>%s</p>
"""
