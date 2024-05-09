import email_validator
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, IntegerField, SelectMultipleField, RadioField, HiddenField
from wtforms.validators import DataRequired, Email, Length, URL, Optional, EqualTo


class SignUpForm(FlaskForm):
    """Forms for user to sign up"""
    first_name = StringField("First Name", validators = [DataRequired()])
    last_name = StringField("Last Name", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class EditProfileForm(FlaskForm):
    """form for a user to edit"""
    first_name = StringField("First Name", validators = [DataRequired()])
    last_name = StringField("Last Name", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])

class LoginForm(FlaskForm):
    """Form to login as a user"""
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class AddLink(FlaskForm):
    """form to add link"""
    platform = StringField("Platform", validators = [DataRequired()])
    link = StringField("Link", validators = [DataRequired(), URL()])

