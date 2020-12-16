import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aslu*+98yv!5269luiyv%^gfz)#rsgh'
    WTF_CSRF_SECRET_KEY = "dsgliubsr8511v/?!khyvdv"
    MONGODB_SETTINGS = {'db': 'UTA_Enrollment'}  #, 'host': 'mongodb://localhost:27017/UTA_Enrollment'

# Tutorial video:   https://www.linkedin.com/learning/full-stack-web-development-with-flask/