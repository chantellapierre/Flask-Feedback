from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = StringField("Password", validators = [InputRequired()])
    email = StringField("Email", validators = [InputRequired()])
    first_name = StringField("First Name", validators = [InputRequired()])
    last_name = StringField("Last Name", validators = [InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = StringField("Password", validators = [InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=50)])
    content = StringField("Content", validators=[InputRequired(), Length(max=250)])

class DeleteForm(FlaskForm):