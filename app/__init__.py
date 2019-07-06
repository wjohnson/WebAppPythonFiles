from flask import Flask
from config import Config

appvar = Flask(__name__, static_folder="static")
appvar.config.from_object(Config)

from app import routes
