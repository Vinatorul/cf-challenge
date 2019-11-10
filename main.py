import os
import sys
import datetime
import time
import functools
import hashlib
import random
import secret
from sqlalchemy import Column, Integer, String, DateTime
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('cf-challange.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
#app.config['SERVER_NAME'] = # NAME
#app.config['SERVER_PORT'] = # Port
db = SQLAlchemy(app)

def print_err(s):
    print(s, file=sys.stderr)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('include/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('include/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('include/fonts', path)

@app.route('/', methods = ["GET", "POST"])
def root():
    contestId = '258990' 
    rnd = str(random.randrange(100000, 1000000))
    tm = str(int(time.time()))
    params = ['apiKey=' + secret.cfpubkey, 'contestId=' + str(contestId), 'time=' + tm]
    req = '/contest.standings?'
    hs = rnd + req + '&'.join(params) + '#' + secret.cfsecretkey
    hs = hs.encode('utf-8')
    hs = str(hashlib.sha512(hs).hexdigest())
    ref = "https://codeforces.com/api" + req + "&".join(params)
    ref += '&apiSig=' + rnd + hs
    return '<a href="' + ref + '">codef</a>'
