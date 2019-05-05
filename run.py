# run.py
import os
from app import create_app
import configuration

app = create_app(configuration.DevelopmentConfig)

