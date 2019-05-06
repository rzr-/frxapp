from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import login_manager
from . import app
# db variable initialization
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    # Create an User table
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sign_up_date = db.Column(db.Date)
    activated  = db.Column(db.Integer, default=0)
    notifications = db.Column(db.Integer, default=1)
    type = db.Column(db.Integer, default=0)

    @property
    def password(self):
        # Prevent pasword from being accessed
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        # Set password to a hashed password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Check if hashed password matches actual password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Signal(db.Model):
    # Create a Signal table
    __tablename__ = 'signals'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16))
    element = db.Column(db.String(16))
    entry = db.Column(db.String(16))
    take_profit = db.Column(db.String(16))
    stop_loss = db.Column(db.String(16))
    share_with = db.Column(db.Integer)
    date_added = db.Column(db.Date)
    date_expiry = db.Column(db.Date)

    def __repr__(self):
        return '<Signal: {}>'.format(self.type)
