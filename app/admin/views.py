# app/admin/views.py
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import SignalForm, UserEditForm
# from .. import db
from ..models import Signal, User, db

from datetime import datetime, timedelta, timezone
from ..auth import views as mailing

typeDict = {'long': 'Long',
            'short': 'Short',
            'buyStop': 'Buy stop',
            'sellStop': 'Sell stop',
            'buyLimit': 'Buy limit',
            'sellLimit': 'Sell limit'}

def check_admin():
    #Prevent non-admins from accessing the page
    if current_user.type != 2:
        abort(403)

def send_signal_to_users(signal):
    html = render_template('email/signal.html', signal=signal, typeDict=typeDict)
    subject = "FRXapp | New Signal!"
    mailing.send_email("axel.hilmi@mail.ru", subject, html)
    mailing.send_email("axel.adem@gmail.com", subject, html)

# Signal Views
@admin.route('/signals', methods=['GET', 'POST'])
@login_required
def list_signals():
    # List all signals
    check_admin()

    signals = Signal.query.all()
    return render_template('admin/signals/signals.html',
                            signals=signals,
                            title="Signals",
                            typeDict=typeDict)


@admin.route('/signals/add', methods=['GET', 'POST'])
@login_required
def add_signal():
    # Add a signal to the database
    check_admin()

    add_signal = True

    form = SignalForm()
    if form.validate_on_submit():
        signal = Signal(type=form.type.data,
                        element=form.element.data,
                        entry=form.entry.data,
                        take_profit=form.take_profit.data,
                        stop_loss=form.stop_loss.data,
                        share_with=form.share_with.data,
                        date_added=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
                        date_expiry=datetime.now(timezone.utc) + timedelta(minutes=form.date_expiry.data)
                        )
        try:
            # add signal to the database
            db.session.add(signal)
            db.session.commit()
            flash('You have successfully added a new signal.')

            send_signal_to_users(signal)
        except:
            flash('Error 60.')
        # redirect to signals page
        return redirect(url_for('admin.list_signals'))

    # load signal template
    return render_template('admin/signals/signal.html',
                            action="Add",
                            add_signal=add_signal,
                            form=form,
                            title="Add Signal")


@admin.route('/signals/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_signal(id):
    # Edit a signal
    check_admin()

    add_signal = False

    signal = Signal.query.get_or_404(id)
    form = SignalForm(obj=signal)

    datetime_end = datetime.strptime(signal.date_expiry.strftime("%d-%m-%Y %H:%M"), "%d-%m-%Y %H:%M")
    datetime_start = datetime.strptime(signal.date_added.strftime("%d-%m-%Y %H:%M"), "%d-%m-%Y %H:%M")
    minutes_diff = (datetime_end - datetime_start).total_seconds() / 60.0
    form.date_expiry.data = int(minutes_diff)

    if form.validate_on_submit():
        signal.type = form.type.data
        signal.element = form.element.data
        signal.entry = form.entry.data
        signal.take_profit = form.take_profit.data
        signal.stop_loss = form.stop_loss.data
        signal.share_with = form.share_with.data
        signal.date_added = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        signal.date_expiry = datetime.now(timezone.utc) + timedelta(minutes=form.date_expiry.data)
        db.session.commit()
        flash('You have successfully edited the signal.')

        send_signal_to_users(signal)
        # redirect to the signals page
        return redirect(url_for('admin.list_signals'))

    return render_template('admin/signals/signal.html',
                            action="Edit",
                            add_signal=add_signal,
                            form=form,
                            signal=signal,
                            title="Edit Signal")

@admin.route('/signals/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_signal(id):
    #Delete a signal from the database
    check_admin()

    signal = Signal.query.get_or_404(id)
    db.session.delete(signal)
    db.session.commit()
    flash('You have successfully deleted the signal.')

    # redirect to the signals page
    return redirect(url_for('admin.list_signals'))

    return render_template(title="Delete Signal")

@admin.route('/users')
@login_required
def list_users():
    #List all users
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')

@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    #Edit user
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    #if employee.is_admin:
    #    abort(403)

    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.fist_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.notifications = form.notifications.data
        if user.type != 2:
            user.type = form.type.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully edited user.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                            user=user,
                            form=form,
                            title='Edit User')

@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    #Delete user
    check_admin()

    #user = User.query.get_or_404(id)
    #User.query.filter_by(id=123).delete()
    User.query.filter(User.id == id).delete()
    db.session.commit()
    flash('You have successfully deleted user.', 'success')
    #users = User.query.all()
    return redirect(url_for('admin.list_users'))
    #return render_template('admin/users/users.html', users=users, title='Users')