# run.py
import os
from app import create_app
import configuration

config_name = os.getenv('FLASK_CONFIG')
app = create_app(configuration.DevelopmentConfig)
