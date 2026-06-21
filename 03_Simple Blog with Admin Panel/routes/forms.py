from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    name = StringField("Enter Your Name", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Enter Your Email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter Your Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Register")

class LogInForm(FlaskForm):
    email = EmailField("Enter Your Email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter Your Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class BlogForm(FlaskForm):
    title = StringField("Blog Title", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post Blog")
