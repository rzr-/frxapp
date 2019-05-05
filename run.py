# run.py
import os
from app import create_app
import configuration

from flask.ext.heroku import Heroku

app = create_app(configuration.DevelopmentConfig)
heroku = Heroku(app)
