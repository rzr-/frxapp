# app/user/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email

class UserEditForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    notifications =  SelectField('Notifications', choices=[ ('0', 'Disabled'),
                        ('1', 'Enabled')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class PasswordForm(FlaskForm):
    current_pass = PasswordField('Current Password', validators=[DataRequired()])
    new_pass = PasswordField('New Password', validators=[DataRequired()])
    new_pass_repated = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Change')