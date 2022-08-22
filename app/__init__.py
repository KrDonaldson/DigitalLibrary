from flask import Flask

app = Flask(__name__)

from .site.routes import site

app.register_blueprint(site)