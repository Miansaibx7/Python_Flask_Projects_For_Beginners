from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=20),
        Regexp(r"^[a-zA-Z0-9_]+$", message="Username must contain only letters, numbers, or underscores")
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class ResendVerificationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Resend Verification Email")

class PasswordResetRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

class PasswordResetForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")

class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description")
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    category = StringField("Category", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Save Product")

class CheckoutForm(FlaskForm):
    address = TextAreaField("Shipping Address", validators=[DataRequired()])
    submit = SubmitField("Proceed to Payment")