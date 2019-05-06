# app/user/views.py
from flask import flash, redirect, render_template, url_for, current_app, Markup
from flask_login import current_user, login_required
from .forms import UserEditForm, PasswordForm
from . import user
# from .. import db
from ..models import Signal, User, db
from ..auth import views as auth
from itsdangerous import URLSafeTimedSerializer

def flash_please_activate():
    if current_user.is_authenticated and current_user.activated == 0:
        flash (Markup('Please, activate your account. <a href="' + url_for('auth.resend') + '">Click here to resend</a>'), 'error')

@user.route('/user/signals', methods=['GET', 'POST'])
@login_required
def list_signals():
    #List all signals
    #TODO LIST ONLY BASIC OR PREMIUM
    #check_user()
    if current_user.type == 0:
        signals = Signal.query.filter_by(share_with=0)
    else:
        signals = Signal.query.all()
    typeDict = {'long': 'Long',
                'short': 'Short',
                'buyStop': 'Buy stop',
                'sellStop': 'Sell stop',
                'buyLimit': 'Buy limit',
                'sellLimit': 'Sell limit'}
    flash_please_activate()
    return render_template('user/signals/signals.html',
                           signals=signals, title="Signals", typeDict=typeDict)

@user.route('/user/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    # Edit user
    #check_admin()

    user = User.query.get_or_404(current_user.get_id())

    form_useredit = UserEditForm(obj=user)
    if form_useredit.validate_on_submit():
        user.first_name = form_useredit.first_name.data
        user.last_name = form_useredit.last_name.data
        user.notifications = form_useredit.notifications.data

        if user.email != form_useredit.email.data:
            user.email = form_useredit.email.data
            user.activated = 0

            token = auth.generate_confirmation_token(user.email)
            confirm_url = url_for('user.confirm_email', token=token, _external=True)
            html = render_template('email/activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            auth.send_email(user.email, subject, html)
            flash('A confirmation email has been sent via email.', 'success')

        db.session.add(user)
        db.session.commit()
        flash('You have successfully changed settings.', 'success')

        #return redirect(url_for("home.dashboard"))
    flash_please_activate()
    return render_template('user/settings/settings.html',
                           user=user,
                           form_useredit=form_useredit,
                           title='Settings')

@user.route('/user/settings/reset', methods=['GET', 'POST'])
@login_required
def user_password_reset():
    user = User.query.get_or_404(current_user.get_id())

    form_password = PasswordForm(obj=user)
    if form_password.validate_on_submit():
        if (user.verify_password(form_password.current_pass.data)):
            if (form_password.new_pass.data == form_password.new_pass_repated.data):
                user.password = form_password.new_pass.data
                db.session.add(user)
                db.session.commit()
                flash('You have successfully changed password.', 'success')
                # redirect to the roles page
                # return redirect(url_for('home.dashboard'))
            else:
                flash('Password does not match the confirm password.', 'error')
        else:
            flash('Wrong current password.', 'error')

    flash_please_activate()
    return render_template('user/settings/password_reset.html',
                           form_password=form_password,
                           title='Password Reset')

@user.route('/confirm/<token>')
#@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
    user = User.query.filter_by(email=email).first_or_404()
    if user.activated == 1:
        flash('Account already activated. Please login.', 'success')
    else:
        user.activated = 1
        #user.activated_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have activated your account. Thanks!', 'success')
        if current_user.is_authenticated:
            return redirect(url_for('home.dashboard'))
    return redirect(url_for('auth.login'))

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email