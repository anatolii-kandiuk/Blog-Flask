from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError, InputRequired
from flask_login import current_user
from .models import User
from .. import bcrypt


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

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                       Length(min=4, max=14, message='Length of username must be between 4 and 14'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]+$', message='Username must contains only letters, numbers, dot or underline')])

    email = StringField('Email', validators=[DataRequired(), Email('Email is incorrect!')])

    picture = FileField('Update profile picture',
                        validators=[FileAllowed(['jpg', 'png'])])

    about_me = TextAreaField('About Me', validators=[DataRequired(), Length(max=500)])

    submit_button = SubmitField(label=(''))

    def validate_email(self, field):
        if field.data != current_user.email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Inputed email is already exist in the system!')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Inputed username is already exist in the system!')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])

    new_password = PasswordField('Password', validators=[InputRequired('Password is required'),
                                                          Length(min=6, message='Must be at least 6')])

    r_new_password = PasswordField('Repeat the password', validators=[InputRequired('Password is required'),
                                                                     Length(min=6, message='Must be at least 6'),
                                                                     EqualTo('new_password')])
    submit_button = SubmitField(label=(''))

    def validate_old_password(self, field):
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('Error')
