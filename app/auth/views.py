# app/auth/views.py
from datetime import datetime, timezone
from flask import flash, redirect, render_template, url_for, current_app, request, Markup
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm, PasswordResetForm, EmailForm
# from .. import db
from ..models import User, db

################################################
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

def flash_please_activate():
    if current_user.is_authenticated and current_user.activated == 0:
        flash (Markup('Please, activate your account. <a href="' + url_for('auth.resend') + '">Click here to resend</a>'), 'error')

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail = Mail(current_app)
    mail.send(msg)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
################################################

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home.dashboard"))
    # Handle requests to the /register route
    # Add an user to the database through the registration form
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=form.password.data,
                    sign_up_date=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                    #activated='0',
                    #notifications='1',
                    #type='0'
                    )

        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! Welcome.', 'success')
        ################################################
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('email/activate.html', confirm_url=confirm_url)
        subject = "FRXapp | Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        ################################################
        # redirect to the login page
        return redirect(url_for("home.dashboard"))
        # return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.dashboard"))
    # Handle requests to the /login route
    # Log an user in through the login form
    next = request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():
        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log user in
            login_user(user)
            if next:
                return redirect(next)
            # redirect to the appropriate dashboard page
            if user.type == 2:
                return redirect(url_for('home.admin_dashboard'))
            else:
                #flash_please_activate()
                return redirect(url_for('home.dashboard'))
        # when login details are incorrect
        else:
            flash('Invalid email or password.', 'error')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    # Handle requests to the /logout route
    # Log an user out through the logout link
    logout_user()
    flash('You have successfully been logged out.', 'success')
    # redirect to the login page
    return redirect(url_for('auth.login'))

@auth.route('/resend', methods=['GET', 'POST'])
def resend():
    if current_user.activated == 1:
        return redirect(url_for("home.dashboard"))

    if current_user.is_authenticated:
        if current_user.activated == 0:
            token = generate_confirmation_token(current_user.email)
            confirm_url = url_for('user.confirm_email', token=token, _external=True)
            html = render_template('email/activate.html', confirm_url=confirm_url)
            subject = "FRXapp | Please confirm your email"
            try:
                send_email(current_user.email, subject, html)
                flash('An activation email has been sent via email.', 'success')
            except:
                flash('Please check your email address and try again.', 'error')

    return redirect(url_for("home.dashboard"))

@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for("home.dashboard"))
    form = EmailForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('Please check your email address and try again.', 'error')
            return render_template('auth/reset/email_form.html', form=form)

        if user.activated == 1:
            send_password_reset_email(user.email)
            flash('Please check your email for a password reset link.', 'success')
        else:
            flash('Your email address must be confirmed before attempting a password reset.', 'error')
            return redirect(url_for('auth.resend'))

    return render_template('auth/reset/email_form.html', form=form)

def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    password_reset_url = url_for(
        'auth.reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt=current_app.config['SECURITY_PASSWORD_SALT']),
        _external=True)

    html = render_template('email/password_reset.html', password_reset_url=password_reset_url)
    subject = 'FRXapp | Password Reset Requested'
    send_email(user_email, subject, html)

@auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Please check your email address and try again.', 'error')
            return redirect(url_for('auth.login'))

        if (form.new_pass.data == form.new_pass_repated.data):
            user.password = form.new_pass.data
            db.session.add(user)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Password does not match the confirm password', 'error')

    return render_template('auth/reset/password_form.html', form=form, token=token)

