# app/admin/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class SignalForm(FlaskForm):
    # Form for admin to add or edit a signal

    type = SelectField('Type', choices=[
            ('long', 'Long'),
            ('short', 'Short'),
            ('buyStop', 'Buy stop'),
            ('sellStop', 'Sell stop'),
            ('buyLimit', 'Buy limit'),
            ('sellLimit', 'Sell limit')], validators=[DataRequired()])
    element = SelectField('Instrument',choices=[
            ('EURUSD', 'EURUSD'),
            ('GBPUSD', 'GBPUSD'),
            ('USDJPY', 'USDJPY'),
            ('USDCHF', 'USDCHF'),
            ('USDCAD', 'USDCAD')], validators=[DataRequired()])

    entry = StringField('Entry', validators=[DataRequired()])
    take_profit = StringField('Take Profit', validators=[DataRequired()])
    stop_loss = StringField('Stop Loss', validators=[DataRequired()])
    share_with = SelectField('Share with', choices=[('0', 'Basic'), ('1', 'Premium')], validators=[DataRequired()])
    #date = StringField('Date')
    date_expiry = IntegerField('Minutes to expire', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserEditForm(FlaskForm):
    # Form for admin to edit user

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    notifications =  SelectField('Notifications', choices=[ ('0', 'Disabled'),
                        ('1', 'Enabled')], validators=[DataRequired()])
    type = SelectField('Type', choices=[ ('0', 'Basic'),
                        ('1', 'Premium')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class PasswordForm(FlaskForm):
    current_pass = PasswordField('Current Password', validators=[DataRequired()])
    new_pass = PasswordField('New Password', validators=[DataRequired()])
    new_pass_repated = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Change')