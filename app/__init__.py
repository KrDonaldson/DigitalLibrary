from flask import Flask
from config import Config
from .site.routes import site
from .auth.routes import auth

app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)

app.config.from_object(Config)