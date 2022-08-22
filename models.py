from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, username='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Book(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(150), nullable = False)
    author = db.Column(db.String(150), nullable = False)
    pages = db.Column(db.Integer, nullable = True, default = 1)
    isbn = db.Column(db.String(50), nullable = True, default = '')
    dewey = db.Column(db.String(50), nullable = True, default = '')
    edition = db.Column(db.String(50), nullable = True, default = '')
    publisher = db.Column(db.String(150), nullable = True, default = '')
    date_published = db.Column(db.Date, nullable = True)
    cover = db.Column(db.Integer, nullable = True, default = 1)
    subjects = db.Column(db.String(150), nullable = True, default = '')
    description = db.Column(db.Text, nullable = True, default = '')
    series = db.Column(db.String(150), nullable = True, default = '')
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,title, author, pages, isbn, dewey, edition, publisher, date_published, cover, subjects, decription, series, user_token, id = ''):
        self.id = self.set_id()
        self.title = title
        self.author = author 
        self.pages = pages 
        self.isbn = isbn 
        self.dewey =dewey 
        self.edition = edition
        self.publisher = publisher
        self.date_published = date_published
        self.cover = cover
        self.subjects = subjects
        self.decription = decription
        self.series = series
        self.user_token = user_token

    def __repr__(self):
        return f'The following book has been added to your library: {self.title} by {self.author}'

    def set_id(self):
        return (secrets.token_urlsafe())

class BookSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'author', 'pages', 'isbn', 'dewey', 'edition', 'publisher', 'date_published', 'cover', 'subjects', 'decription', 'series']

book_schema = BookSchema()
books_schema = BookSchema(many=True)
