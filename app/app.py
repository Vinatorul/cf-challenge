from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from models import *
import os

ALLOWED_EXTENSIONS = set(['jpg'])
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('cf-challenge.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


login_manager = LoginManager(app)
db = SQLAlchemy(app)



