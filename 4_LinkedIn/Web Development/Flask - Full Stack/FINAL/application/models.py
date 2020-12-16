from application import db
from werkzeug.security import generate_password_hash, check_password_hash


#-------------------------------------------------------------------------------------
# Mongo DB management
class User(db.Document):
    user_id     = db.IntField(unique = True)
    first_name  = db.StringField(max_lenght = 50)
    last_name   = db.StringField(max_lenght=50)
    # area        = db.StringField(max_lenght=3)
    email       = db.StringField(max_lenght=30, unique = True)
    password    = db.StringField( )
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def get_password(self, password):
        return check_password_hash(self.password, password)

class Course(db.Document):
    courseID    = db.StringField(unique = True, max_lenght = 10)
    title       = db.StringField(max_lenght=100)
    description = db.StringField(max_lenght=225)
    credits     = db.IntField()
    term        = db.StringField(max_lenght=25)

class Enrollment(db.Document):
    user_id     = db.IntField()
    courseID    = db.StringField(max_lenght=10)
