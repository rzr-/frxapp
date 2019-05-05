# app/home/views.py
from flask import abort, render_template, flash, Markup, url_for
from flask_login import current_user, login_required

from . import home

def flash_please_activate():
    if current_user.is_authenticated and current_user.activated == 0:
        flash (Markup('Please, activate your account. <a href="' + url_for('auth.resend') + '">Click here to resend</a>'), 'error')

@home.route('/')
def homepage():
    # Render the homepage template on the / route
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    # Render the dashboard template on the /dashboard route
    flash_please_activate()
    return render_template('home/dashboard.html', title="Dashboard")

# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if current_user.type != 2:
        abort(403)
    return render_template('home/admin_dashboard.html', title="Dashboard")