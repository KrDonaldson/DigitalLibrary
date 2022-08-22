from flask import Flask
from .site.routes import site
from config import Config

app = Flask(__name__)

app.register_blueprint(site)

app.config.from_object(Config)