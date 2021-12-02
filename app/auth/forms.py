from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                       Length(min=4, max=14, message='Length of username must be between 4 and 14'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]+$', message='Username must contains only letters, numbers, dot or underline')])

    email = StringField('Email', validators=[DataRequired(), Email('Email is incorrect!')])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Minimal length of password is 6 symbols')])

    password_confirmation = PasswordField('Confirm password',
                                          validators=[DataRequired(), EqualTo('password')])

    submit_button = SubmitField(label=(''))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Inputed email is already exist in the system!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Inputed username is already exist in the system!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Email is incorrect!')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField(label=(''))