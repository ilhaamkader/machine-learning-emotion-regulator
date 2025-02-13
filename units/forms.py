from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class UserEmotionDescription(FlaskForm):
    description = StringField("Describe the emotion you want to feel",validators=[DataRequired()])
    submitfield = SubmitField(label="CONFIRM")