import os
import sys
import datetime
import time
import functools
import hashlib
import random
import secret
import requests
from sqlalchemy import Column, Integer, String, DateTime
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('cf-challange.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
#app.config['SERVER_NAME'] = # NAME
#app.config['SERVER_PORT'] = # Port
db = SQLAlchemy(app)

class Contestant(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(10000), unique=True)
    name = Column(String(10000))

    def __init__(self, handle, name):
        self.handle = handle
        self.name = name

class Contest(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(10000))

    def __init__(self, id, name):
        self.id = id
        self.name = name

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

def get_data(cfdata):
    contest = cfdata['contest']
    problems = cfdata['problems']
    problems_count = len(problems)
    rows = cfdata['rows']
    result = 'Информация по контесту ' + contest['name']
    if contest['phase'] == 'FINISHED':
        result += '(Завершен)'
    result += '<table class="table table-striped">'
    result += '<thead class="thead-dark">'
    result += '<tr>'
    result += '<th scope="col">Участник</th>' 
    for i in range(problems_count):
        result += '<th scope="col">' + chr(i + ord("A")) + '</th>'
    result += '<th scope="col">Челлендж</th>'
    result += '</tr>'
    result += '</thead><tbody>'
    for r in rows:
        percent = int(r['points'] / problems_count * 100)
        if percent >= 80:
            result += '<tr class="table-success">'
        else:
            result += '<tr>'
        result += '<th scope="row">'
        handle = r['party']['members'][0]['handle']
        contestant = Contestant.query.filter_by(handle=handle).first()
        if contestant:
            result += contestant.name  
        else:
            result += handle
        result += '</td>'
        problem_res = r['problemResults']
        for pr in problem_res:
            result += '<td>'
            if pr['points'] > 0:
                result += '+'
                if pr['rejectedAttemptCount'] > 0:
                    result += str(pr['rejectedAttemptCount'])
            else:
                if pr['rejectedAttemptCount'] > 0:
                    result += '-' + str(pr['rejectedAttemptCount'])
            result += '</td>'
        result += '<td>'
        if percent >= 80:
            result += 'выполнен (' + str(percent) +'%)'
        else:
            result += 'не выполнен (' + str(percent) +'%)'
        result += '</td>'
        result += '</tr>'
    result += '</tbody></table>'
    return result

def get_contestants_table():
    result = ''
    result += '<table class="table table-striped">'
    result += '<thead class="thead-dark">'
    result += '<tr>'
    result += '<th scope="col">#</th>'
    result += '<th scope="col">Участник</th>' 
    result += '<th scope="col">CF Handle</th>'
    result += '</tr>'
    result += '</thead><tbody>'
    contestants = Contestant.query.order_by(Contestant.name).all()
    i = 0
    for contestant in contestants:
        i += 1
        result += '<tr>'
        result += '<th scope="row">' + str(i) + '</th>' 
        result += '<td>' + contestant.name + '</td>'
        result += '<td><a href="https://codeforces.com/profile/' +\
            contestant.handle + '">' + contestant.handle + '</td>'
        result += '</tr>'
    result += '</tbody></table>'
    return result

@app.route('/contestants', methods = ["GET", "POST"])
def contestants():
    if request.method == 'POST':
        handle = request.form['handle']
        name = request.form['name']
        contestant = Contestant(handle, name)
        db.session.add(contestant)
        db.session.commit()

    
    with open('include/contestants.html', 'r', encoding="utf-8") as page:
        data=page.read()
    data = data.replace('%CONTESTANTS%', get_contestants_table())
    return data 

@app.route('/contest_info/<int:contestId>', methods = ["GET", "POST"])
def contest_info(contestId):
    rnd = str(random.randrange(100000, 1000000))
    tm = str(int(time.time()))
    params = ['apiKey=' + secret.cfpubkey, 'contestId=' + str(contestId), 'time=' + tm]
    req = '/contest.standings?'
    hs = rnd + req + '&'.join(params) + '#' + secret.cfsecretkey
    hs = hs.encode('utf-8')
    hs = str(hashlib.sha512(hs).hexdigest())
    ref = "https://codeforces.com/api" + req + "&".join(params)
    ref += '&apiSig=' + rnd + hs
    response = requests.get(ref)
    cfdata = get_data(response.json()['result']) 

    with open('include/contest_info.html', 'r', encoding="utf-8") as page:
        data=page.read()
    data = data.replace('%CF_DATA%', cfdata)
    return data 


def get_contest_table():
    result = ''
    result += '<table class="table table-striped">'
    result += '<thead class="thead-dark">'
    result += '<tr>'
    result += '<th scope="col">#</th>'
    result += '<th scope="col">Результаты</th>'
    result += '<th scope="col">Результаты на CF</th>'
    result += '</tr>'
    result += '</thead><tbody>'
    contests = Contest.query.all()
    i = 0
    for contest in contests:
        i += 1
        result += '<tr>'
        result += '<th scope="row">' + str(i) + '</th>'
        result += '<td><a href="contest_info/' +\
            str(contest.id) + '">' + contest.name + '</td>'
        result += '<td>https://codeforces.com/group/U9XUJaQnsj/contest/' +\
            str(contest.id) + '</td>'
        result += '</tr>'
    result += '</tbody></table>'
    return result

@app.route('/', methods = ["GET", "POST"])
def root():
    if request.method == 'POST':
        id = request.form['contestId']
        name = request.form['name']
        contest = Contest(id, name)
        db.session.add(contest)
        db.session.commit()

    with open('include/index.html', 'r', encoding="utf-8") as page:
        data=page.read()
    data = data.replace('%CONTESTS%', get_contest_table())
    return data 
