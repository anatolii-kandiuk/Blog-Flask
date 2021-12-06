from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, IntegerField, FloatField, DateField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed

class CreatePC(FlaskForm):
    firm = StringField('Firm', validators=[InputRequired(), Length(min=2, max=60)])
    type_processor = StringField('Type processor', validators=[Length(max=100)])
    clock_frequency = FloatField('Clock frequency', validators=[DataRequired()])
    is_available = BooleanField(label=('Is available'))
    image_file = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    date_created = DateField('Date created')

    category = SelectField(u'Category', coerce=int)

    submit = SubmitField('')

class CategoryForm(FlaskForm):
    ram = IntegerField('Category', validators=[DataRequired()])
    submit = SubmitField('')