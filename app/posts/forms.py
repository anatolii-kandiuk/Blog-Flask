from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import Length, InputRequired
from flask_wtf.file import FileField, FileAllowed

class CreatePost(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=60)])
    text = TextAreaField('Text', validators=[Length(max=2000)])
    image_file = FileField('Add image', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('Type', choices=[('Flask', 'Flask'),
                                        ('Django', 'Django'),
                                        ('Other', 'Other')])
    enabled = BooleanField('Enabled')
    submit = SubmitField(' ')

