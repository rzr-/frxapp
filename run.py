# run.py
import os
from app import create_app, db
import configuration

app = create_app(configuration.DevelopmentConfig)
db.create_all()