from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///" +os.path.join(basedir, "simple_flask.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["DEBUG"]=False

db = SQLAlchemy(app)

#config auth
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)
login_manager.login_view = "login"

from . import views, models, forms