from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from pricetracker.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min = 2, max = 10)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min = 6)])
    conform_password = PasswordField('Conform password',validators=[DataRequired(),Length(min = 6), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already exist.. Please choose another one')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email already exist.. Please choose another one')

class LoginForm(FlaskForm):
    # username = StringField('Username',validators=[DataRequired(),Length(min = 2, max = 10)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(min = 6)])
    # confirm_password = PasswordFied('password',validators=['Conform Password', DataRequired(),Length(min = 6)], EqualTo('password'))
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
class SearchForm(FlaskForm):
    # interval = IntegerField('Price will be checked by system in minutes:',validators=[DataRequired(),NumberRange(min=0, max=10)])
    url = StringField('Copy Url of the website opened with the product you wanna buy...',validators=[DataRequired()])
    target_price = FloatField('Target Price in units as per webpage of product', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # def validate_target_price(self, target_price):
    #     user = User.query.filter_by(username = username.data).first()
    #     if user:
    #         raise ValidationError('Username already exist.. Please choose another one')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min = 2, max = 10)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username already exist.. Please choose another one')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email already exist.. Please choose another one')
