from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlalchemy://Qu1s:@localhost/test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    handle = db.Column(db.String(100), unique =  True)
    name = db.Column(db.String(100))

    def __init(self, handle, name):
        self.handle = handle
        self.name = name



