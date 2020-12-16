from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User


class LoginForm(FlaskForm):
    email       = StringField('Email', validators = [DataRequired(), Email()])
    password    = PasswordField('Password', validators = [DataRequired(), Length(min=3, max=15)])
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Login')

class RegisterForm(FlaskForm):
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=15)])   #tup1911
    password_confirm    = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name  = StringField('First Name', validators=[DataRequired()])
    last_name   = StringField('Last Name')
    # area        = StringField('Geographic Area')
    submit      = SubmitField('Register Now')
    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use")
