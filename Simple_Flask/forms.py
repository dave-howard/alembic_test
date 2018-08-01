from flask_wtf import Form, FlaskForm
from wtforms.validators import DataRequired, url, Length, Regexp, Email, EqualTo, ValidationError
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from Simple_Flask.models import User


class LoginForm(FlaskForm):
    email = StringField('Your Email:',validators=[DataRequired(),
                                              Length(1,120),
                                              Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class SignupForm(FlaskForm):
    password = PasswordField('Password:',
                             validators=[DataRequired(),
                                         EqualTo("password2", message="Passwords must match.")])
    password2 = PasswordField('Confirm password:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(),
                                              Length(1,120),
                                              Email()])
    submit = SubmitField('Sign up')

    @staticmethod
    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There is already a user with this email address.')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password:',
                             validators=[DataRequired(),
                                         EqualTo("password2", message="Passwords must match.")])
    password2 = PasswordField('Confirm password:', validators=[DataRequired()])
    submit = SubmitField('Change Password')