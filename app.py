# import order is determined by Flask, so silencing the warning is ok
# pylint: disable=unused-import, wrong-import-position

from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utilities.date_format import apply_jinja_function

app = Flask(__name__)
app.secret_key = getenv("SESSION_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
apply_jinja_function(app)

from routes import index
from routes import paste
from routes import user
from routes import chat
from routes import votes
from routes import settings
