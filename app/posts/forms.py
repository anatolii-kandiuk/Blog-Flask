from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import Length, InputRequired
from flask_wtf.file import FileField, FileAllowed

class CreatePost(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=60)])
    text = TextAreaField('Text', validators=[Length(max=2000)])
    image = FileField('Add image', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('Type', choices=[('Video', 'Video'),
                                        ('Article', 'Article'),
                                        ('Other', 'Other')])
    category = SelectField(u'Category', validators=[InputRequired()], coerce=str)

    tag = SelectMultipleField(u'Tag', validators=[InputRequired()], coerce=int)
    enabled = BooleanField('Enabled')

    submit = SubmitField('')

class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[InputRequired(), Length(min=2, max=60)])
    submit = SubmitField('')
