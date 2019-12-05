from flask import Flask, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('cf-challange.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    handle = db.Column(db.String(24), unique=True) # Max length of Codeforce's handle = 24 
    name = db.Column(db.String(1000), unique=True)

    def __init__(self, handle, name):
        self.handle = handle
        self.name = name

class Contests(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    contestId = db.Column(db.Integer, unique = True)
    name = db.Column(db.String(1000), unique = True)

    def __init__(self, contestId, name):
        self.contestId = contestId
        self.name = name
